import numpy as np
import time
import pprint
import random
import copy


def swap_board(board, board_map,  ij, ij_):
    val1 = board[ij[0], ij[1]]
    val2 = board[ij_[0], ij_[1]]
    board_map[val2] = copy.deepcopy(ij)
    board_map[val1] = copy.deepcopy(ij_)

    temp = board[ij[0], ij[1]]
    board[ij[0], ij[1]] = board[ij_[0], ij_[1]]
    board[ij_[0], ij_[1]] = temp


def board2map(board):
    res = np.zeros((33, 2))
    for i in range(3):
        for j in range(11):
            res[board[i, j]] = [i, j]
    return res


class GradientDescent:
    def __init__(self, env):
        self.env = env

    def search(self, executiontime):
        etime = executiontime  # 実行時間(この時間回す)
        start = time.time()
        now = start

        # 全ての回中最高のスコア
        best_board = self.env.board.copy()
        best_map = board2map(best_board)
        best_score = self.env.score(best_map)

        # current_score:whileの各回でのはじめのスコア
        current_board = self.env.board.copy()
        current_map = board2map(current_board)
        current_score = self.env.score(current_map)

        count = 0

        while(now-start < etime):
            count += 1

            swap_list = []
            # max_score:各スワップで最も良いスコア(はじめはcurrent_score)
            max_score = current_score
            for i in range(3):
                for j in range(10):
                    # 横のスワップ([i,j]<->[i,j+1])
                    swap_board(current_board, current_map, [i, j], [i, j+1])

                    score = self.env.score(current_map)
                    if(score >= max_score):
                        swap_list.append([[i, j], [i, j+1]])
                        max_score = score

                    swap_board(current_board, current_map, [i, j], [i, j+1])

            for i in range(2):
                for j in range(11):
                    # 縦のスワップ([i,j]<->[i+1,j])
                    swap_board(current_board, current_map, [i, j], [i+1, j])

                    score = self.env.score(current_map)
                    if(score >= max_score):
                        swap_list.append([[i, j], [i+1, j]])
                        max_score = score

                    swap_board(current_board, current_map, [i, j], [i+1, j])

            if(len(swap_list) != 0):
                swap = random.choice(swap_list)
                ij, ij_ = swap[0], swap[1]
                temp = current_board[ij[0], ij[1]]
                current_board[ij[0], ij[1]] = current_board[ij_[0], ij_[1]]
                current_board[ij_[0], ij_[1]] = temp
                current_score = max_score
            else:
                break

            if(count % 10 == 0):
                print(count, current_score)
            now = time.time()

        print("展開数:", count)
        if(now - start > etime):
            print("time over")
        else:
            print(now-start)
        return current_board, current_score


class MountainClimbing:
    def __init__(self, env):
        self.env = env

    def search(self, executiontime):
        etime = executiontime  # 実行限界時間(この時間で打ち切る)
        start = time.time()
        now = start

        # current_score:whileの各回でのはじめのスコア
        current_board = self.env.board.copy()
        current_score = self.env.score(current_board)

        count = 0

        while(now-start < etime):
            count += 1

            swap_list = []
            # max_score:各スワップで最も良いスコア(はじめはcurrent_score)
            max_score = current_score
            for i in range(3):
                for j in range(10):
                    # 横のスワップ([i,j]<->[i,j+1])
                    swap_board(current_board, [i, j], [i, j+1])

                    score = self.env.score(current_board)
                    if(score >= max_score):
                        swap_list.append([[i, j], [i, j+1]])
                        max_score = score

                    swap_board(current_board, [i, j], [i, j+1])

            for i in range(2):
                for j in range(11):
                    # 縦のスワップ([i,j]<->[i+1,j])
                    swap_board(current_board, [i, j], [i+1, j])

                    score = self.env.score(current_board)
                    if(score >= max_score):
                        swap_list.append([[i, j], [i+1, j]])
                        max_score = score

                    swap_board(current_board, [i, j], [i+1, j])

            if(len(swap_list) != 0):
                swap = random.choice(swap_list)
                ij, ij_ = swap[0], swap[1]
                temp = current_board[ij[0], ij[1]]
                current_board[ij[0], ij[1]] = current_board[ij_[0], ij_[1]]
                current_board[ij_[0], ij_[1]] = temp
                current_score = max_score
            else:
                break

            if(count % 10 == 0):
                print(count, current_score)
            now = time.time()

        print("展開数:", count)
        if(now - start > etime):
            print("time over")
        else:
            print(now-start)
        return current_board, current_score


class A_star:
    def __init__(self, env):
        self.env = env

    def search(self):
        goal = [[16, 22, 4, 17, 19, 24, 20, 8, 14, 15, 28],
                [0, 18, 3, 5, 6, 7, 9, 10, 11, 31, 32],
                [26, 25, 23, 2, 21, 1, 13, 12, 29, 30, 27]]
        pprint.pprint(goal)
