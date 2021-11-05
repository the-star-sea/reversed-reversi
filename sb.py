import numpy as np
import random
import time
from numba import njit

corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)
MIN_VALUE = -999999999
MAX_VALUE = 999999999
direction = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
goods = {(0, 1), (0, 6), (1, 0), (1, 7), (6, 0), (6, 7), (7, 1), (7, 6)}


# @njit(fastmath=True, nogil=True, cache=True)
def game_is_finished(chessboard):
    rest = np.where(chessboard == COLOR_NONE)
    rest = list(zip(rest[0], rest[1]))
    return len(rest) == 0


@njit(fastmath=True, nogil=True, cache=True)
def make_next_move(board, x: int, y: int, player: int):
    chessboard = board.copy()
    chessboard[x, y] = player
    for direc in direction:
        ctr = 0
        for i in range(8):
            ox = x + direc[0] * (i + 1)
            oy = y + direc[1] * (i + 1)
            if ox < 0 or ox >= 8 or oy < 0 or oy >= 8:
                ctr = 0
                break
            elif chessboard[ox, oy] == player:
                break
            elif chessboard[ox, oy] == COLOR_NONE:
                ctr = 0
                break
            else:
                ctr += 1
        for i in range(ctr):
            ddx = x + direc[0] * (i + 1)
            ddy = y + direc[1] * (i + 1)
            chessboard[ddx, ddy] = player
    return chessboard


# def generate_legal_point(color, chessboard):
#     rest = np.where(chessboard == COLOR_NONE)
#     rest = list(zip(rest[0], rest[1]))
#     rest = list(filter(lambda x: legalpoint(x, chessboard, color) > 0, rest))
#     return rest


@njit(fastmath=True, nogil=True, cache=True)
def generate_legal_points(color, chessboard):
    rest = np.where(chessboard == COLOR_NONE)
    rest = list(zip(rest[0], rest[1]))
    ss = []
    # rest = list(filter(lambda x: legalpoint(x, chessboard, color) > 0, rest))
    for ob in rest:
        if legalpoint(ob, chessboard, color) > 0:
            ss.append(ob)
    return ss


# @njit(fastmath=True, nogil=True, cache=True)
def mobility(color, chessboard) -> float:
    rest1 = generate_legal_points(color, chessboard)
    rest2 = generate_legal_points(-color, chessboard)
    point = 100 * (len(rest1) - len(rest2)) / (len(rest1) + len(rest2) + 1)
    return point


# @njit(fastmath=True, nogil=True, cache=True)
def evaluate(chessboard, color, min, sta, mb) -> float:
    point = min * piece(color, chessboard) + mb * mobility(color, chessboard)
    if sta > 0:
        point += sta * stability(color, chessboard)
    return point


@njit(fastmath=True, nogil=True, cache=True)
def legalpoint(pos, board, color) -> int:
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
            if board[row + (step + 1) * direction[i][0]][col + (step + 1) * direction[i][1]] == color:
                score += zs
                break
            step += 1
    return score


# @njit(fastmath=True, nogil=True, cache=True)
def piece(color, chessboard):
    rest1 = np.where(chessboard == color)
    rest1 = list(zip(rest1[0], rest1[1]))
    rest2 = np.where(chessboard == -color)
    rest2 = list(zip(rest2[0], rest2[1]))
    a = len(rest1)
    b = len(rest2)
    return 100 * (b - a) / (b + a + 1)


@njit(fastmath=True, nogil=True, cache=True)
def get_stable_pieces(chessboard, color):
    move_list = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    stable_piece_list = []
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    for corner in corners:
        i = corner[0]
        j = corner[1]
        if chessboard[i][j] == color:
            if (i, j) not in stable_piece_list:
                stable_piece_list.append((i, j))
            for move in move_list:
                ni = i + move[0]
                nj = j + move[1]
                while (0 <= ni < 8 and 0 <= nj < 8) and \
                        chessboard[ni][nj] == color:
                    if (ni, nj) not in stable_piece_list:
                        stable_piece_list.append((ni, nj))
                    ni = ni + move[0]
                    nj = nj + move[1]

    return stable_piece_list


# @njit(fastmath=True, nogil=True, cache=True)
def stability(color, chessboard):
    my_score = len(get_stable_pieces(chessboard, color))
    op_score = len(get_stable_pieces(chessboard, -color))

    return 100 * (op_score - my_score) / (op_score + my_score + 1)


# @njit(fastmath=True, nogil=True, cache=True)
# def bestt1(chessboard, color):
#     best = [[(0, 1), (1, 0), (1, 1)], [(0, 6), (1, 6), (1, 7)], [(6, 0), (6, 1), (7, 1)], [(7, 6), (6, 6), (6, 7)]]
#     sum1 = 0
#     sum3 = 0
#     for ob in best:
#         s1 = 0
#         s3 = 0
#         for obb in ob:
#             if chessboard[obb[0]][obb[1]] == color:
#                 s1 += 1
#             if chessboard[obb[0]][obb[1]] == -color:
#                 s3 += 1
#         if s1 == 3:
#             sum1 += 1
#
#         if s3 == 3:
#             sum1 += 1
#
#     return sum1, sum3
#
#
# @njit(fastmath=True, nogil=True, cache=True)
# def bestt(flipped_board, color):
#     best = [[(0, 1), (1, 0), (1, 1)], [(0, 6), (1, 6), (1, 7)], [(6, 0), (6, 1), (7, 1)], [(7, 6), (6, 6), (6, 7)]]
#     sum2 = 0
#     sum4 = 0
#     for ob in best:
#         s2 = 0
#         s4 = 0
#         for obb in ob:
#             if flipped_board[obb[0]][obb[1]] == color:
#                 s2 += 1
#             if flipped_board[obb[0]][obb[1]] == -color:
#                 s4 += 1
#         if s2 == 3:
#             sum2 += 1
#         if s4 == 3:
#             sum2 += 1
#     return sum2, sum4


def doweight(chessboard, color):
    weight = np.array(
        [[100, -70, 8, 6, 6, 8, -70, 100],
         [-70, -40, -4, -4, -4, -4, -40, -70],
         [8, -4, 6, 4, 4, 6, -4, 8],
         [6, -4, 4, 0, 0, 4, -4, 6],
         [6, -4, 4, 0, 0, 4, -4, 6],
         [8, -4, 6, 4, 4, 6, -4, 8],
         [-70, -40, -4, -4, -4, -4, -40, -70],
         [100, -70, 8, 6, 6, 8, -70, 100]])
    if chessboard[0][1] == color:
        weight[1][1] -= 20
        # weight[2][1] -= 5
    if chessboard[1][0] == color:
        weight[1][1] -= 20
        # weight[1][2] -= 5

    if chessboard[0][6] == color:
        weight[1][6] -= 20
        # weight[2][6] -= 5
    if chessboard[1][7] == color:
        weight[1][6] -= 20
        # weight[1][5] -= 5

    if chessboard[6][0] == color:
        weight[6][1] -= 20
        # weight[6][2] -= 5
    if chessboard[7][1] == color:
        weight[6][1] -= 20
        # weight[5][1] -= 5

    if chessboard[6][7] == color:
        weight[6][6] -= 20
        # weight[6][5] -= 5
    if chessboard[7][6] == color:
        weight[6][6] -= 20
        # weight[5][6] -= 5

    # if chessboard[0][1] == color or chessboard[7][1] == color:
    #     weight[1][1] -= 40
    #     weight[6][1] -= 40
    # if chessboard[0][6] == color or chessboard[7][6] == color:
    #     weight[1][6] -= 40
    #     weight[6][6] -= 40
    # if chessboard[1][0] == color or chessboard[1][7] == color:
    #     weight[1][1] -= 40
    #     weight[1][6] -= 40
    # if chessboard[6][0] == color or chessboard[6][7] == color:
    #     weight[6][1] -= 40
    #     weight[6][6] -= 40

    # if (chessboard[0][1] == color) or (chessboard[7][1] == color):
    #     weight[1][1] -= 30
    # if chessboard[0][6] == color or chessboard[7][6] == color:
    #     weight[6][6] -= 30
    # if chessboard[1][0] == color or chessboard[1][7] == color:
    #     weight[1][6] -= 30
    # if chessboard[6][0] == color or chessboard[6][7] == color:
    #     weight[6][1] -= 30
    return weight


class AI(object):
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.candidate_list = []
        self.mb = 4
        self.sta = 0
        self.weigh = 5
        self.min = 4
        self.corner = 200
        # self.good = 10
        self.weight = np.array(
            [[100, -60, 8, 6, 6, 8, -60, 100],
             [-60, -40, -4, -4, -4, -4, -40, -60],
             [8, -4, 6, 4, 4, 6, -4, 8],
             [6, -4, 4, 0, 0, 4, -4, 6],
             [6, -4, 4, 0, 0, 4, -4, 6],
             [8, -4, 6, 4, 4, 6, -4, 8],
             [-60, -40, -4, -4, -4, -4, -40, -60],
             [100, -60, 8, 6, 6, 8, -60, 100]])

    # def __init__(self, chessboard_size, color, time_out,weigh,gain):
    #     self.chessboard_size = chessboard_size
    #     self.color = color
    #     self.time_out = time_out
    #     self.candidate_list = []
    #     self.weigh=weigh
    #     self.gain=gain
    def go(self, chessboard):
        self.time_out = time.time() + 4.8
        # self.candidate_list.clear()
        self.candidate_list = generate_legal_points(self.color, chessboard)
        move_list = self.candidate_list.copy()
        rest = np.where(chessboard == COLOR_NONE)
        rest = list(zip(rest[0], rest[1]))
        if self.color == COLOR_BLACK:
            if len(rest) < 8:
                self.min = 4
                self.mb = 0
                self.sta = 4
                self.weigh = 0
                self.corner = 0
                self.gogo(8, move_list, chessboard, 4)
            # elif len(rest) < 16:
            #     self.mb = 4.5
            #     self.sta = 0
            #     self.weigh = 1.5
            #     self.min = 5
            #     self.weight=np.array([
            #         [100, -40, 8, 6, 6, 8, -40, 100],
            #         [-40, -45, -4, -4, -4, -4, -45, -40],
            #         [8, -4, 6, 4, 4, 6, -4, 8],
            #         [6, -4, 4, 0, 0, 4, -4, 6],
            #         [6, -4, 4, 0, 0, 4, -4, 6],
            #         [8, -4, 6, 4, 4, 6, -4, 8],
            #         [-40, -45, -4, -4, -4, -4, -45, -40],
            #         [100, -40, 8, 6, 6, 8, -40, 100]
            #     ])
            #     self.gogo(8, move_list, chessboard, 3)
            elif len(rest) < 24:
                self.mb = 4
                self.sta = 0
                self.weigh = 2.5
                self.min = 4
                self.corner = 200
                self.weight = doweight(chessboard, self.color)
                self.gogo(9, move_list, chessboard, 3)
            # elif len(rest) < 32:
            #     self.mb = 6
            #     self.sta = 0
            #     self.weigh = 3.5
            #     self.min = 5
            #     self.gogo(8, move_list, chessboard, 3)
            elif len(rest) < 48:
                self.mb = 4.5
                self.sta = 0
                self.weigh = 2
                self.min = 4
                self.corner = 200
                self.weight = doweight(chessboard, self.color)
                self.gogo(7, move_list, chessboard, 3)
            else:
                self.mb = 4.5
                self.sta = 0
                self.weigh = 2
                self.min = 4
                self.corner = 200
                self.weight = doweight(chessboard, self.color)
                self.gogo(7, move_list, chessboard, 3)
        else:
            if len(rest) < 8:
                self.min = 4
                self.mb = 0
                self.sta = 4
                self.weigh = 0
                self.corner = 0
                self.gogo(8, move_list, chessboard, 4)
            # elif len(rest) < 16:
            #     self.mb = 4.5
            #     self.sta = 0
            #     self.weigh = 1.5
            #     self.min = 5
            #     self.weight = np.array([
            #         [100, -40, 8, 6, 6, 8, -40, 100],
            #         [-40, -45, -4, -4, -4, -4, -45, -40],
            #         [8, -4, 6, 4, 4, 6, -4, 8],
            #         [6, -4, 4, 0, 0, 4, -4, 6],
            #         [6, -4, 4, 0, 0, 4, -4, 6],
            #         [8, -4, 6, 4, 4, 6, -4, 8],
            #         [-40, -45, -4, -4, -4, -4, -45, -40],
            #         [100, -40, 8, 6, 6, 8, -40, 100]
            #     ])
            #     self.gogo(8, move_list, chessboard, 3)
            elif len(rest) < 24:
                self.mb = 5.5
                self.sta = 0
                self.weigh = 2.5
                self.min = 4
                self.corner = 200
                self.weight = doweight(chessboard, self.color)
                self.gogo(9, move_list, chessboard, 3)
            elif len(rest) < 48:
                self.mb = 5.5
                self.sta = 0
                self.weigh = 3
                self.min = 4
                self.corner = 200
                self.weight = doweight(chessboard, self.color)
                self.gogo(7, move_list, chessboard, 3)
            else:
                self.mb = 4.5
                self.sta = 0
                self.weigh = 2.5
                self.min = 4
                self.corner = 200
                self.weight = doweight(chessboard, self.color)
                self.gogo(7, move_list, chessboard, 3)
            return self.candidate_list

    def min_value(self, chessboard, color, depth, alpha, beta):
        if time.time() > self.time_out:
            return evaluate(chessboard, self.color, self.min, self.sta, self.mb)
        if depth <= 0 or game_is_finished(chessboard):
            return evaluate(chessboard, self.color, self.min, self.sta, self.mb)

        best_score = MAX_VALUE

        move_list = generate_legal_points(color, chessboard)
        if len(move_list) > 0:
            for move in move_list:
                new_board = make_next_move(chessboard, move[0], move[1], color)
                new_score = self.max_value(new_board, -color, depth - 1, alpha, beta)
                if move in corners:
                    new_score += self.corner
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
                new_board = make_next_move(chessboard, move[0], move[1], color)
                new_score = self.min_value(new_board, -color, depth - 1, alpha, beta)
                if move in corners:
                    new_score -= self.corner
                best_score = max(best_score, new_score)
                if best_score >= beta:
                    return best_score
                alpha = max(alpha, best_score)
            return best_score
        else:
            new_score = self.min_value(chessboard, -color, depth - 1, alpha, beta)
            return new_score

    def gogo(self, maxdep, move_list, chessboard, depth):
        leng = len(move_list)
        # sum1, sum3 = bestt1(chessboard, self.color)
        if leng > 1:
            while True:
                if time.time() > self.time_out or depth > maxdep:
                    break
                best_score = MIN_VALUE
                best_move = None

                for move in move_list:
                    new_board = make_next_move(chessboard, move[0], move[1], self.color)
                    c = self.min_value(new_board, -self.color, depth, MIN_VALUE, MAX_VALUE)
                    new_score = c - self.weigh * self.weight[move[0]][move[1]]
                    if move in corners:
                        new_score -= 500
                    # sum2, sum4 = bestt(new_board, self.color)
                    # if sum2 + sum3 > sum1 + sum4:
                    #     new_score += 50
                    if new_score >= best_score:
                        best_score = new_score
                        best_move = move
                if leng == len(self.candidate_list) and best_score > MIN_VALUE:
                    self.candidate_list.append(best_move)

                if time.time() < self.time_out and best_score > MIN_VALUE:
                    self.candidate_list.append(best_move)
                    depth += 2

