import numpy as np
from nbb import AI1,make_next_move
from sb import AI
import random

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0

def contest1():
    chessboard = np.zeros((8, 8))
    chessboard[3, 3] = 1
    chessboard[3, 4] = -1
    chessboard[4, 3] = -1
    chessboard[4, 4] = 1
    black = AI1(8, -1, 5)
    white = AI(8, 1, 5)
    while True:
        rest = np.where(chessboard == 0)
        rest = list(zip(rest[0], rest[1]))
        if (len(rest)) == 0:
            break


        black.go(chessboard)
        white.go(chessboard)

        if (len(black.candidate_list) > 0):
            pos = black.candidate_list.pop()
            chessboard = make_next_move(chessboard, pos[0], pos[1], COLOR_BLACK)
        if (len(white.candidate_list) > 0):
            pos = white.candidate_list.pop()
            chessboard = make_next_move(chessboard, pos[0], pos[1], COLOR_WHITE)
    rest1 = np.where(chessboard == COLOR_BLACK)
    rest1 = list(zip(rest1[0], rest1[1]))
    print(len(rest1) -(64-len(rest1)))
    chessboard = np.zeros((8, 8))
    chessboard[3, 3] = 1
    chessboard[3, 4] = -1
    chessboard[4, 3] = -1
    chessboard[4, 4] = 1
    black = AI(8, -1, 5)
    white = AI1(8, 1, 5)
    while True:
        rest = np.where(chessboard == 0)
        rest = list(zip(rest[0], rest[1]))
        if (len(rest)) == 0:
            break


        black.go(chessboard)
        white.go(chessboard)

        if (len(black.candidate_list) > 0):
            pos = black.candidate_list.pop()
            chessboard = make_next_move(chessboard, pos[0], pos[1], COLOR_BLACK)
        if (len(white.candidate_list) > 0):
            pos = white.candidate_list.pop()
            chessboard = make_next_move(chessboard, pos[0], pos[1], COLOR_WHITE)
    rest1 = np.where(chessboard == COLOR_BLACK)
    rest1 = list(zip(rest1[0], rest1[1]))
    print(len(rest1) - (64 - len(rest1)))
    return
def contest(b1, b2, w1, w2):
    chessboard = np.zeros((8, 8))
    chessboard[3, 3] = 1
    chessboard[3, 4] = -1
    chessboard[4, 3] = -1
    chessboard[4, 4] = 1

    chessboard = np.array(
        [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 1, -1, 0, 0, 0],
         [0, 0, 0, -1, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]
         ])
    while True:
        rest = np.where(chessboard == 0)
        rest = list(zip(rest[0], rest[1]))
        if (len(rest)) == 0:
            break
        black = AI(8, -1, 5, b1, b2)
        white = AI(8, 1, 5, w1, w2)
        black.go(chessboard)
        white.go(chessboard)
        if (len(black.candidate_list) > 0):
            pos = black.candidate_list.pop()
            chessboard = make_next_move(chessboard, pos[0], pos[1], COLOR_BLACK)
        if (len(white.candidate_list) > 0):
            pos = white.candidate_list.pop()
            chessboard = make_next_move(chessboard, pos[0], pos[1], COLOR_WHITE)
    rest1 = np.where(chessboard == COLOR_BLACK)
    rest1 = list(zip(rest1[0], rest1[1]))
    return len(rest1) > 32



if __name__ == "__main__":
    contest1()
    # all = []
    # point = []
    # all.append((1, 8))
    # point.append(0)
    # for i in range(49):
    #     all.append((random.uniform(0,5), (random.uniform(0, 20))))
    #     point.append(0)
    # print(all)
    # for i in range(50):
    #     print(i)
    #     print(point)
    #     for j in range(i + 1, 50):
    #         if contest(all[i][0], all[i][1], all[j][0], all[j][1]):
    #             point[i] += 1
    #
    #         else:
    #             point[j] += 1
    #
    #         if contest(all[j][0], all[j][1], all[i][0], all[i][1]):
    #             point[j] += 1
    #
    #         else:
    #             point[i] += 1
    #         print(point)
    #
    # dic = dict(zip(all, point))
    # all = sorted(all, key=lambda x: dic[x])
    # print(all[:10])
