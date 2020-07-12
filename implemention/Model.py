import numpy as np
import time
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


class SimulatedAnnealing:
    def __init__(self, env):
        self.env = env

    def t(self, time, etime, temp_num):
        res = 0
        if temp_num == 1:  # 線形
            res = max(200-time/20, 0.05)
        elif temp_num == 2:  # 対数
            pass
        return res

    def swap_prob(self, dif_score, time, etime, temp_num):  # prob = exp(-E/t)
        prob = 1/np.exp(dif_score/self.t(time, etime, temp_num))
        return prob

    def search(self, executiontime, score_num, temp_num):
        etime = executiontime  # 実行時間(この時間回す)
        start = time.time()
        now = start

        # 全ての回中最高のスコア
        best_board = self.env.board.copy()
        best_map = board2map(best_board)
        best_score = self.env.score(best_map, score_num)

        # current_score:whileの各回でのはじめのスコア
        current_board = self.env.board.copy()
        current_map = board2map(current_board)
        current_score = self.env.score(current_map, score_num)

        count = 0
        dif = [0]*30
        while(self.t(count, etime, temp_num) > 1e-5):
            count += 1

            # # # # # スワップ処理 # # # # #

            flag = random.random() > 0.5
            i = j = 0
            if flag:  # 横向きのスワップ
                i, j = random.randint(0, 2), random.randint(0, 9)
                swap_board(current_board, current_map, [i, j], [i, j+1])
                score = self.env.score(current_map, score_num)
                swap_board(current_board, current_map, [i, j], [i, j+1])
            else:  # 縦向きのスワップ
                i, j = random.randint(0, 1), random.randint(0, 10)
                swap_board(current_board, current_map, [i, j], [i+1, j])
                score = self.env.score(current_map, score_num)
                swap_board(current_board, current_map, [i, j], [i+1, j])

            if current_score > score:
                dif[int(min((current_score - score), 29))] += 1

            prob = self.swap_prob(current_score-score, count, etime, temp_num)\
                if current_score > score else 1

            swap_or_not = prob >= random.random()
            if swap_or_not:
                if flag:
                    swap_board(current_board, current_map, [i, j], [i, j+1])
                else:
                    swap_board(current_board, current_map, [i, j], [i+1, j])
                current_score = score
                if current_score > best_score:
                    best_score = current_score
                    best_map = current_map  # copyしないでも多分大丈夫
                    best_board = current_board  # copyしないでも多分大丈夫

            # # # # # スワップ処理終了 # # # # #

            if count % 100 == 0:
                print(count, current_score, best_score, prob)

            if count % 1000 == 0:  # 差の期待値
                a = dif/np.sum(dif)
                exp = 0
                for i in range(len(dif)):
                    exp += 100*i*a[i]
                print(exp)

            now = time.time()

        print("展開数:", count)
        if now - start > etime:
            print("time over")
        else:
            print(now-start)
        return best_board, best_score


class MountainClimbing:
    def __init__(self, env):
        self.env = env

    def search(self, executiontime, score_num, exec_num):
        etime = executiontime  # 実行限界時間(この時間内で打ち切る)
        start = time.time()
        now = start

        # current_score:whileの各回でのはじめのスコア
        current_board = self.env.board.copy()
        current_map = board2map(current_board)
        current_score = self.env.score(current_map, score_num)

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

                    score = self.env.score(current_map, score_num)
                    if score > max_score:
                        swap_list = [[[i, j], [i, j+1]]]
                        max_score = score
                    elif score == max_score:
                        swap_list.append([[i, j], [i, j+1]])

                    swap_board(current_board, current_map, [i, j], [i, j+1])

            for i in range(2):
                for j in range(11):
                    # 縦のスワップ([i,j]<->[i+1,j])
                    swap_board(current_board, current_map, [i, j], [i+1, j])

                    score = self.env.score(current_map, score_num)
                    if score > max_score:
                        swap_list = [[[i, j], [i+1, j]]]
                        max_score = score
                    elif score == max_score:
                        swap_list.append([[i, j], [i+1, j]])

                    swap_board(current_board, current_map, [i, j], [i+1, j])

            if len(swap_list) != 0:
                swap = random.choice(swap_list)
                ij, ij_ = swap[0], swap[1]
                swap_board(current_board, current_map, ij, ij_)
                current_score = max_score
            else:
                break

            if count % 10 == 0:
                print(count, current_score)
            now = time.time()

        print("展開数:", count)
        if now - start > etime:
            print("time over")
        else:
            print(now-start)
        return current_board, current_score
