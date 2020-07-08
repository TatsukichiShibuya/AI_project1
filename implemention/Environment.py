import numpy as np
import random
import pprint


class Environment:
    def __init__(self, setting):
        # qwerty配列
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

        # 評価用の文字列
        self.line = "I've seen horrors horrors that you've seen." +\
            " But you have no right to call me a murderer." +\
            " You have a right to kill me." +\
            " You have a right to do that" +\
            " but you have no right to judge me." +\
            " It's impossible for words to describe" +\
            " what is necessary to those who do not know what horror means." +\
            " Horror." +\
            " Horror has a face and you must make a friend of horror." +\
            " Horror and moral terror are your friends." +\
            " If they are not then they are enemies to be feared." +\
            " They are truly enemies." +\
            " I remember when I was with Special Forces." +\
            " Seems a thousand centuries ago." +\
            " We went into a camp to inoculate the children." +\
            " We left the camp after" +\
            " we had inoculated the children for Polio" +\
            " and this old man came running after us and he was crying." +\
            " He couldn't see." +\
            " We went back there and they had come and" +\
            " hacked off every inoculated arm." +\
            " There they were in a pile." +\
            " A pile of little arms." +\
            " And I remember I I I cried." +\
            " I wept like some grandmother." +\
            " I wanted to tear my teeth out." +\
            " I didn't know what I wanted to do." +\
            " And I want to remember it." +\
            " I never want to forget it." +\
            " I never want to forget." +\
            " And then I realized like I was shot" +\
            " like I was shot with a diamond" +\
            " a diamond bullet right through my forehead." +\
            " And I thought My God the genius of that." +\
            " The genius." +\
            " The will to do that." +\
            " Perfect, genuine, complete, crystalline, pure." +\
            " And then I realized they were stronger than we." +\
            " Because they could stand that these were not monsters." +\
            " These were men trained cadres." +\
            " These men who fought with their hearts," +\
            " who had families, who had children," +\
            " who were filled with love but" +\
            " they had the strength the strength to do that." +\
            " If I had ten divisions of those men" +\
            " our troubles here would be over very quickly." +\
            " You have to have men who are moral" +\
            " and at the same time who are able to utilize" +\
            " their primordial instincts to kill without feeling" +\
            " without passion without judgment without judgment." +\
            " Because it's judgment that defeats us."
        self.line = self.line.lower().split(" ")
        print("評価文字列")
        pprint.pprint(self.line)

        # 文字と数字の対応(a:0 z:25 ':26 ,:27 .:28)
        self.table = np.arange(0, 123)
        self.table -= ord('a')
        num = 26
        for i in ["'", ",", "."]:
            self.table[ord(i)] = num
            num += 1

    def score(self, board_map):  # スコア関数(勾配降下用、単語の連続した文字の距離の和)
        score = 0
        for word in self.line:
            for i in range(1, len(word)):
                a, b = self.table[ord(word[i])], self.table[ord(word[i-1])]
                score += abs(board_map[a, 0]-board_map[b, 0])**2
                score += abs(board_map[a, 1]-board_map[b, 1])**2
        return score

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
