import numpy as np
import random
import pprint


class Environment:
    def __init__(self, setting):
        self.size = map(int, setting[0:2])
        h, w = tuple(self.size)
        assert h >= 3 and w >= 10, "H >= 3 and W >= 10"

        # 初期化用の配列作成
        self.initial = setting[2]
        if(self.initial == 'random'):
            key = random.sample(list(np.arange(1, 34)), 33)
        elif(self.initial == 'qwerty'):
            key = [[], [], []]
        else:
            print(self.initial+' is invalid, initialize with "random"')
            key = random.sample(list(np.arange(1, 34)), 33)

        # boardの初期化
        self.board = [[0 for i in range(w)]for j in range(h)]
        h_, w_ = h//3, w//11
        for i in range(3):
            for j in range(11):
                self.board[i*h_][j*w_] = key[11*i+j]
        print("初期配列")
        pprint.pprint(self.board)

    def value(self, board):
        pass
