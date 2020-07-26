import numpy as np
import time
import random
import copy
from Environment import showBoard


def swapBoard(board, board_map,  ij, ij_):
    val1 = board[ij[0], ij[1]]
    val2 = board[ij_[0], ij_[1]]
    board_map[val2] = copy.deepcopy(ij)
    board_map[val1] = copy.deepcopy(ij_)

    temp = board[ij[0], ij[1]]
    board[ij[0], ij[1]] = board[ij_[0], ij_[1]]
    board[ij_[0], ij_[1]] = temp


def board2map(board):
    res = np.zeros((30, 2))
    for i in range(3):
        for j in range(10):
            res[board[i, j]] = [i, j]
    return res


class SimulatedAnnealing:
    def __init__(self, env):
        self.env = env

    def t(self, t, time, temp_num):  # temperature function
        res = 0
        if temp_num == 1:  # linear
            res = max((1500000-49.98*time)/30000, 3.02-0.02*time/200)
        elif temp_num == 2:  # exponential
            a = 0.99973923
            res = t*a
        return res

    def swapProb(self, dif_score, t):  # transition probability
        prob = 1/np.exp(dif_score/t)
        return prob

    def search(self, exec_time, temp_num):
        if temp_num == 1:
            print("Temperature Function:Linear")
        elif temp_num == 2:
            print("Temperature Function:Exponential")
        etime = exec_time
        start = time.time()
        now = start

        best_board = self.env.board.copy()
        best_map = board2map(best_board)
        best_score = self.env.score(best_map)

        current_board = self.env.board.copy()
        current_map = board2map(current_board)
        current_score = self.env.score(current_map)

        count = 0
        t = 50
        while(t > 1e-2 and now-start < etime):
            count += 1
            t = self.t(t, count, temp_num)

            # # # # # swap processing # # # # #
            flag = random.random() < 27/(20+27)
            i = j = 0
            if flag:  # swap of horizontal
                i, j = random.randint(0, 2), random.randint(0, 8)
                swapBoard(current_board, current_map, [i, j], [i, j+1])
                score = self.env.score(current_map)
                swapBoard(current_board, current_map, [i, j], [i, j+1])
            else:  # swap of vertical
                i, j = random.randint(0, 1), random.randint(0, 9)
                swapBoard(current_board, current_map, [i, j], [i+1, j])
                score = self.env.score(current_map)
                swapBoard(current_board, current_map, [i, j], [i+1, j])

            prob = self.swapProb(current_score-score, t)\
                if current_score > score else 1

            swap_or_not = prob >= random.random()
            if swap_or_not:
                if flag:
                    swapBoard(current_board, current_map, [i, j], [i, j+1])
                else:
                    swapBoard(current_board, current_map, [i, j], [i+1, j])
                current_score = score
                if current_score > best_score:
                    best_score = current_score
                    best_map = current_map
                    best_board = current_board
            # # # # # swap processing # # # # #

            if count % 100 == 0:
                print("Expansion Times:"+str(count), end=' ')
                print("Score:"+str(current_score), end=' ')
                print("Best Score:"+str(best_score))

            now = time.time()

        print()
        if now - start > etime:
            print("TIME's UP")
        else:
            print("FINISH")
            print(str(int((now-start)*10)/10)+"[s]")
        print("Expansion Times(Evaluation Times):"+str(count))
        return best_board, best_score


class MountainClimbing:
    def __init__(self, env):
        self.env = env

    def search(self, exec_time, exec_num):
        etime = exec_time
        start = time.time()
        now = start

        # best score of whole search
        best_board = self.env.board.copy()
        best_map = board2map(best_board)
        best_score = self.env.score(best_map)

        count_sum = 0

        for k in range(exec_num):

            count = 0
            current_board = self.env.board.copy()
            current_map = board2map(current_board)
            current_score = self.env.score(current_map)
            print("Search-"+str(k+1))
            showBoard(current_board)

            while(now-start < etime):
                count += 1

                # # # # # swap processing # # # # #
                swap = []
                max_score = current_score
                for i in range(3):
                    for j in range(9):
                        # swap of horizontal ([i,j]<->[i,j+1])
                        swapBoard(current_board, current_map,
                                  [i, j], [i, j+1])

                        score = self.env.score(current_map)
                        if score > max_score:
                            swap = [[i, j], [i, j+1]]
                            max_score = score

                        swapBoard(current_board, current_map,
                                  [i, j], [i, j+1])

                for i in range(2):
                    for j in range(10):
                        # swap of vertical ([i,j]<->[i+1,j])
                        swapBoard(current_board, current_map,
                                  [i, j], [i+1, j])

                        score = self.env.score(current_map)
                        if score > max_score:
                            swap = [[i, j], [i+1, j]]
                            max_score = score

                        swapBoard(current_board, current_map,
                                  [i, j], [i+1, j])

                if len(swap) != 0:
                    ij, ij_ = swap[0], swap[1]
                    swapBoard(current_board, current_map, ij, ij_)
                    current_score = max_score
                else:
                    break
                # # # # # swap processing # # # # #

                if count % 10 == 0:
                    print("Expansion Times:"+str(count), end=' ')
                    print("Score:"+str(current_score))
                now = time.time()

            count_sum += count

            print("Search-"+str(k+1)+"-Result")
            showBoard(current_board)
            print("Score")
            print(current_score, end='\n\n')
            if current_score > best_score:
                best_score = current_score
                best_map = current_map
                best_board = current_board

            self.env.initializeBoard('random')

        if now - start > etime:
            print("TIME's UP")
        else:
            print("FINISH")
            print(str(int((now-start)*10)/10)+"[s]")
        print("Evaluation Times:", count_sum*47)
        return best_board, best_score
