import time
import pprint
import random


class GradientDescent:
    def __init__(self, env):
        self.env = env

    def search(self, executiontime):
        etime = executiontime  # 実行時間(この時間回す)
        start = time.time()
        now = start
        while(now-start < etime):

            now = time.time()
        best = self.env.board
        return best


class MountainClimbing:
    def __init__(self, env):
        self.env = env

    def search(self, executiontime):
        etime = executiontime  # 実行限界時間(この時間で打ち切る)
        start = time.time()
        now = start

        # best_board = self.env.board.copy()
        # best_score = self.env.score(best_board)

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

                    temp = current_board[i, j]
                    current_board[i, j] = current_board[i, j+1]
                    current_board[i, j+1] = temp

                    score = self.env.score(current_board)
                    if(score >= max_score):
                        swap_list.append([[i, j], [i, j+1]])
                        max_score = score

                    temp = current_board[i, j]
                    current_board[i, j] = current_board[i, j+1]
                    current_board[i, j+1] = temp

            for i in range(2):
                for j in range(11):
                    # 縦のスワップ([i,j]<->[i+1,j])

                    temp = current_board[i, j]
                    current_board[i, j] = current_board[i+1, j]
                    current_board[i+1, j] = temp

                    score = self.env.score(current_board)
                    if(score >= max_score):
                        swap_list.append([[i, j], [i+1, j]])
                        max_score = score

                    temp = current_board[i, j]
                    current_board[i, j] = current_board[i+1, j]
                    current_board[i+1, j] = temp

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
