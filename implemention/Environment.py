import numpy as np
import random
import pprint
import glob
import os


class Environment:

    def __init__(self, setting):
        self.count = 1  # デバッグ用

        # qwerty配列
        self.qwerty = np.array([[16, 22, 4, 17, 19, 24, 20, 8, 14, 15, 28],
                                [0, 18, 3, 5, 6, 7, 9, 10, 11, 31, 32],
                                [26, 25, 23, 2, 21, 1, 13, 12, 29, 30, 27]],
                               dtype=np.uint8)

        # 初期化用の配列作成
        self.board = np.zeros((3, 11), dtype=np.uint8)
        self.initializeBoard(setting[0])
        print("初期配列")
        pprint.pprint(self.board)

        # 評価用の文字列
        texts = glob.glob(os.path.join("text", "*.txt"))
        for filepath in texts:
            text = open(filepath)
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
        if(initial == 'random'):
            key = random.sample(list(np.arange(0, 33)), 33)

        elif(initial == 'qwerty'):
            key = np.reshape(self.qwerty, (33,))

        else:
            print(initial+' is invalid, initialize with "random"')
            key = random.sample(list(np.arange(1, 34)), 33)

        # boardの初期化
        for i in range(3):
            for j in range(11):
                self.board[i, j] = key[11*i+j]

    def score(self, board_map):  # スコア関数(勾配降下用、単語の連続した文字の距離の和)
        score = 0
        for i in range(1, len(self.line)):
            a, b = self.table[ord(self.line[i])],\
                self.table[ord(self.line[i-1])]
            score += abs(board_map[a, 0]-board_map[b, 0])**2
            score += abs(board_map[a, 1]-board_map[b, 1])**2
        return score/len(self.line)

    def score1(self, board_map):  # デバッグ用
        self.count += 1
        return self.count

    def heuristic(self, board):  # ヒューリステック関数(A*用、qwertyとの誤差)
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
