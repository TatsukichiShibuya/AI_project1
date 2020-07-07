import numpy as np
import random
import pprint


class Environment:
    def __init__(self, setting):
        self.qwerty = np.array([[16, 22, 4, 17, 19, 24, 20, 8, 14, 15, 28],
                                [0, 18, 3, 5, 6, 7, 9, 10, 11, 31, 32],
                                [26, 25, 23, 2, 21, 1, 13, 12, 29, 30, 27]],
                               dtype=np.uint8)

        # 初期化用の配列作成
        self.initial = setting[0]
        if(self.initial == 'random'):
            key = random.sample(list(np.arange(0, 33)), 33)
        elif(self.initial == 'qwerty'):
            key = np.reshape(self.qwerty, (33,))
        else:
            print(self.initial+' is invalid, initialize with "random"')
            key = random.sample(list(np.arange(1, 34)), 33)

        # boardの初期化
        self.board = np.zeros((3, 11), dtype=np.uint8)
        for i in range(3):
            for j in range(11):
                self.board[i, j] = key[11*i+j]
        print("初期配列")
        pprint.pprint(self.board)

    def score(self, board):  # スコア関数(勾配降下用、考え中)
        score = 0
        for val in range(33):
            bx = by = qx = qy = 0
            for i in range(3):
                for j in range(11):
                    if(board[i, j] == val):
                        bx, by = i, j
            for i in range(3):
                for j in range(11):
                    if(self.qwerty[i, j] == val):
                        qx, qy = i, j
            score -= (abs(qx-bx)**2+abs(qy-by)**2)
        return score

    def heuristic(self, board):  # ヒューリステック関数(A*用、qwertyとの誤差)
        return len(board[board == self.qwerty])
