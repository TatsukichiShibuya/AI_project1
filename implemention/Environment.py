import numpy as np
import random
import pprint
import glob
import os


class Environment:
    def __init__(self, initial):
        # qwerty配列
        self.qwerty = np.array([[16, 22, 4, 17, 19, 24, 20, 8, 14, 15],
                                [0, 18, 3, 5, 6, 7, 9, 10, 11, 26],
                                [25, 23, 2, 21, 1, 13, 12, 27, 28, 29]],
                               dtype=np.uint8)
        # dvorak配列
        self.dvorak = np.array([[26, 27, 28, 15, 24, 5, 6, 2, 17, 11],
                                [0, 14, 4, 20, 8, 3, 7, 19, 13, 18],
                                [29, 16, 9, 10, 23, 1, 12, 22, 21, 25]],
                               dtype=np.uint8)

        # 初期化用の配列作成
        self.board = np.zeros((3, 10), dtype=np.uint8)
        self.initializeBoard(initial)
        print("初期配列")
        pprint.pprint(self.board)

        # 評価用の文字列
        texts = glob.glob(os.path.join("text", "*.txt"))
        for filepath in texts:
            text = open(filepath)  # あとでlineを配列に変える
        self.line = text.read()
        self.line = self.line.lower()
        print("評価文字列")
        print(self.line)

        # 文字と数字の対応(a:0 - z:25 ':26 ,:27 .:28 space:29)
        self.table = np.arange(0, 1000)
        self.table -= ord('a')
        num = 26
        for i in ["'", ",", ".", " "]:
            self.table[ord(i)] = num
            num += 1

    def initializeBoard(self,  initial):
        # 初期化の種類
        if initial == 'random':
            key = random.sample(list(np.arange(0, 30)), 30)

        elif initial == 'qwerty':
            key = np.reshape(self.qwerty, (30,))
        elif initial == 'dvorak':
            key = np.reshape(self.dvorak, (30,))
        else:
            print(initial+' is invalid, initialize with "random"')
            key = random.sample(list(np.arange(0, 30)), 30)

        # boardの初期化
        for i in range(3):
            for j in range(10):
                self.board[i, j] = key[10*i+j]

    def score(self, board_map):  # スコア関数(勾配降下用、単語の連続した文字の距離の和)
        score = 0

        for i in range(1, len(self.line)):
            a, b = self.table[ord(self.line[i])],\
                self.table[ord(self.line[i-1])]
            # 横距離の和(大きい方が楽)
            score += abs(board_map[a, 1]-board_map[b, 1])**2
            # 縦位置の罰則(二段目が楽)
            score -= (abs(board_map[a, 0]-1)*3)**2

        score /= len(self.line)
        return score
