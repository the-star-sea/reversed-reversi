import numpy as np
import random
import time
from numba import njit,jit

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)
MIN_VALUE = -999999999
MAX_VALUE = 999999999
direction = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
# weight = np.array(
#     [[100, -50, 8, 6, 6, 8, -50, 100],
#      [-50, -75, -4, -4, -4, -4, -75, -50],
#      [8, -4, 6, 4, 4, 6, -4, 8],
#      [6, -4, 4, 0, 0, 4, -4, 6],
#      [6, -4, 4, 0, 0, 4, -4, 6],
#      [8, -4, 6, 4, 4, 6, -4, 8],
#      [-50, -75, -4, -4, -4, -4, -75, -50],
#      [100, -50, 8, 6, 6, 8, -50, 100]])
weight = np.array([
    [100, -10,  8,  6,  6,  8, -10, 100],
    [-10, -25, -4, -4, -4, -4, -25, -10],
    [  8,  -4,  6,  4,  4,  6,  -4,   8],
    [  6,  -4,  4,  0,  0,  4,  -4,   6],
    [  6,  -4,  4,  0,  0,  4,  -4,   6],
    [  8,  -4,  6,  4,  4,  6,  -4,   8],
    [-10, -25, -4, -4, -4, -4, -25, -10],
    [100, -10,  8,  6,  6,  8, -10, 100]
])

@njit
def game_is_finished(chessboard):
    rest = np.where(chessboard == COLOR_NONE)
    rest = list(zip(rest[0], rest[1]))
    return len(rest) == 0


@njit
def make_next_move(board, x: int, y: int, player: int):
    chessboard = board.copy()
    chessboard[x, y] = player
    for direc in direction:
        ctr = 0
        for i in range(8):
            dx = x + direc[0] * (i + 1)
            dy = y + direc[1] * (i + 1)
            if dx < 0 or dx >= 8 or dy < 0 or dy >= 8:
                ctr = 0
                break
            elif chessboard[dx, dy] == player:
                break
            elif chessboard[dx, dy] == COLOR_NONE:
                ctr = 0
                break
            else:
                ctr += 1
        for i in range(ctr):
            ddx = x + direc[0] * (i + 1)
            ddy = y + direc[1] * (i + 1)
            chessboard[ddx, ddy] = player
    return chessboard


@njit
def generate_legal_points(color, chessboard)-> int:
    rest = np.where(chessboard == COLOR_NONE)
    rest = list(zip(rest[0], rest[1]))
    ss=[]
    # rest = list(filter(lambda x: legalpoint(x, chessboard, color) > 0, rest))
    for ob in rest:
        if legalpoint(ob, chessboard, color) > 0:
            ss.append(ob)
    return ss



def mobility(color, chessboard)-> int:
    rest1 = generate_legal_points(color, chessboard)
    rest2 = generate_legal_points(-color, chessboard)
    return len(rest1) - len(rest2)


def evaluate(chessboard, color, min, sta, mb):
    if sta==0:
        point = min * piece(color, chessboard) + mb * mobility(color, chessboard)
    else:
        point = min * piece(color, chessboard) \
            + sta * stability(chessboard, color)+mb*mobility(color,chessboard)
    return point


@njit
def legalpoint(pos, board, color):
    score = 0
    row = pos[0]
    col = pos[1]
    for i in range(8):
        zs = 0
        step = 1
        while (0 <= (row + (step + 1) * direction[i][0]) < 8) and (
                0 <= (col + (step + 1) * direction[i][1]) < 8) and (
                board[row + step * direction[i][0]][col + step * direction[i][1]] == -color):
            zs += 1
            if (board[row + (step + 1) * direction[i][0]][col + (step + 1) * direction[i][1]] == color):
                score += zs
                break
            step += 1
    return score


@njit
def piece(color, chessboard):
    rest1 = np.where(chessboard == color)
    rest1 = list(zip(rest1[0], rest1[1]))
    rest2 = np.where(chessboard == -color)
    rest2 = list(zip(rest2[0], rest2[1]))
    return len(rest2) - len(rest1)


@njit
def get_stable_pieces(chessboard, color):
    chessboard_size = 8

    corner_list = [(0, 0), (0, chessboard_size - 1), (chessboard_size - 1, 0),
                   (chessboard_size - 1, chessboard_size - 1)]
    move_list = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    stable_piece_list = []

    for corner in corner_list:
        i = corner[0]
        j = corner[1]
        if chessboard[i][j] == color:
            if (i, j) not in stable_piece_list:
                stable_piece_list.append((i, j))
            for move in move_list:
                mi = i + move[0]
                mj = j + move[1]
                while (0 <= mi < chessboard_size and 0 <= mj < chessboard_size) and \
                        chessboard[mi][mj] == color:
                    if (mi, mj) not in stable_piece_list:
                        stable_piece_list.append((mi, mj))
                    mi = mi + move[0]
                    mj = mj + move[1]

    return stable_piece_list


def stability(chessboard, color):
    my_score = len(get_stable_pieces(chessboard, color))
    op_score = len(get_stable_pieces(chessboard, -color))

    return op_score - my_score


# def weightc(color, chessboard):
#     rest = np.where(chessboard == color)
#     rest = list(zip(rest[0], rest[1]))
#     point = 0
#     for ob in rest:
#         point += weight[ob[0]][ob[1]]
#     return point
#
#
# def weightpoint(color, chessboard):
#     return weightc(-color, chessboard) - weightc(color, chessboard)


class AI1(object):
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.candidate_list = []
        self.min = 1
        self.weigh = 1
        self.gain = 8
        self.mb = 10
        self.sta = 0

    # def __init__(self, chessboard_size, color, time_out,weigh,gain):
    #     self.chessboard_size = chessboard_size
    #     self.color = color
    #     self.time_out = time_out
    #     self.candidate_list = []
    #     self.weigh=weigh
    #     self.gain=gain
    def go(self, chessboard):
        self.time_out = time.time() + 4.8
        move_list, dic = self.generate_legal_point(self.color, chessboard)
        self.candidate_list = move_list.copy()
        rest = np.where(chessboard == COLOR_NONE)
        rest = list(zip(rest[0], rest[1]))
        if len(rest) <8:
            self.min=3
            self.mb = 5
            self.sta = 5
            self.weigh = 1
            self.gain = 0
            self.gogo(8, move_list, chessboard, dic,4)
        if len(rest)<48:
            self.mb=10
            self.sta = 0
            self.weigh = 3
            self.gain = 20
            self.min = 4
            self.gogo(5, move_list, chessboard, dic,4)
        else:
            self.mb = 10
            self.sta = 0
            self.weigh = 1
            self.gain = 8
            self.gogo(5, move_list, chessboard, dic,4)

    def generate_legal_point(self, color, chessboard):
        rest = np.where(chessboard == COLOR_NONE)
        rest = list(zip(rest[0], rest[1]))
        legeldic = {x: legalpoint(x, chessboard, color) for x in rest}
        rest = list(filter(lambda x: legalpoint(x, chessboard, color) > 0, rest))
        return rest, legeldic

    def min_value(self, chessboard, color, depth, alpha, beta):
        if time.time() > self.time_out:
            return evaluate(chessboard, self.color, self.min, self.sta, self.mb)
        if depth <= 0 or game_is_finished(chessboard):
            return evaluate(chessboard, self.color, self.min, self.sta, self.mb)

        best_score = MAX_VALUE

        move_list = generate_legal_points(color, chessboard)
        if len(move_list) > 0:
            for move in move_list:
                flipped_board = make_next_move(chessboard, move[0], move[1], color)
                new_score = self.max_value(flipped_board, -color, depth - 1, alpha, beta)

                best_score = min(best_score, new_score)
                if best_score <= alpha:
                    return best_score
                beta = min(beta, best_score)
            return best_score
        else:
            new_score = self.max_value(chessboard, -color, depth - 1, alpha, beta)
            return new_score

    def max_value(self, chessboard, color, depth, alpha, beta):
        if time.time() > self.time_out:
            return evaluate(chessboard, self.color, self.min, self.sta, self.mb)
        if depth <= 0 or game_is_finished(chessboard):
            return evaluate(chessboard, self.color, self.min, self.sta, self.mb)

        best_score = MIN_VALUE

        move_list = generate_legal_points(color, chessboard)
        if len(move_list) > 0:
            for move in move_list:
                flipped_board = make_next_move(chessboard, move[0], move[1], color)
                new_score = self.min_value(flipped_board, -color, depth - 1, alpha, beta)
                best_score = max(best_score, new_score)
                if best_score >= beta:
                    return best_score
                alpha = max(alpha, best_score)
            return best_score
        else:
            new_score = self.min_value(chessboard, -color, depth - 1, alpha, beta)
            return new_score



    def gogo(self, maxdep, move_list, chessboard, dic,depth):
        leng = len(move_list)
        if leng > 1:
            while True:
                if time.time() > self.time_out or depth > maxdep:
                    break
                best_score = MIN_VALUE
                best_move = None
                for move in move_list:
                    flipped_board = make_next_move(chessboard, move[0], move[1], self.color)
                    c = self.min_value(flipped_board, -self.color, depth, MIN_VALUE, MAX_VALUE)
                    new_score = self.min * c - self.weigh * weight[move[0]][move[1]] - self.gain * dic[move]
                    if new_score >= best_score:
                        best_score = new_score
                        best_move = move
                if leng == len(self.candidate_list) and best_score > MIN_VALUE:
                    self.candidate_list.append(best_move)

                if time.time() < self.time_out and best_score > MIN_VALUE:
                    self.candidate_list.append(best_move)
                    depth += 1
