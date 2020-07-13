import numpy as np
import random
import pprint
import os


class Environment:
    def __init__(self, initial):
        # qwerty
        self.qwerty = np.array([[16, 22, 4, 17, 19, 24, 20, 8, 14, 15],
                                [0, 18, 3, 5, 6, 7, 9, 10, 11, 26],
                                [25, 23, 2, 21, 1, 13, 12, 27, 28, 29]],
                               dtype=np.uint8)
        # dvorak
        self.dvorak = np.array([[26, 27, 28, 15, 24, 5, 6, 2, 17, 11],
                                [0, 14, 4, 20, 8, 3, 7, 19, 13, 18],
                                [29, 16, 9, 10, 23, 1, 12, 22, 21, 25]],
                               dtype=np.uint8)

        # board for initializing
        self.board = np.zeros((3, 10), dtype=np.uint8)
        self.initializeBoard(initial)
        print("Initial Board")
        pprint.pprint(self.board)
        print()

        # string for evaluating
        text = open(os.path.join("text", "text1.txt"))
        self.line = text.read()
        self.line = self.line.lower()
        print("String for Evaluation")
        print(self.line)
        print()

        # making map(a:0 - z:25 ':26 ,:27 .:28 space:29)
        self.table = np.arange(0, 1000)
        self.table -= ord('a')
        num = 26
        for i in ["'", ",", ".", " "]:
            self.table[ord(i)] = num
            num += 1

    def initializeBoard(self,  initial):
        if initial == 'random':
            key = random.sample(list(np.arange(0, 30)), 30)

        elif initial == 'qwerty':
            key = np.reshape(self.qwerty, (30,))
        elif initial == 'dvorak':
            key = np.reshape(self.dvorak, (30,))
        else:
            print(initial+' is invalid, initialize with "random"')
            key = random.sample(list(np.arange(0, 30)), 30)

        # initialize board
        for i in range(3):
            for j in range(10):
                self.board[i, j] = key[10*i+j]

    def score(self, board_map):  # score function
        score = 0

        for i in range(1, len(self.line)):
            a, b = self.table[ord(self.line[i])],\
                self.table[ord(self.line[i-1])]
            score += abs(board_map[a, 1]-board_map[b, 1])**2
            score -= (abs(board_map[a, 0]-1)*3)**2

        score /= len(self.line)
        return score
