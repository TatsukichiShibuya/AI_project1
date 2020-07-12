from Environment import Environment
from Model import SimulatedAnnealing, MountainClimbing, board2map
import argparse
import pprint


def main(**kwargs):

    if kwargs['model'] in ['1', '2']:  # 探索
        env = Environment(kwargs['setting'][0])
        arg1, arg2 = int(kwargs['setting'][1]), int(kwargs['setting'][2])

        if kwargs['model'] == '1':  # 焼き鈍し法
            model = SimulatedAnnealing(env)
            assert arg1 in [1, 2] and arg2 in[1, 2], "wrong setting"
        elif kwargs['model'] == '2':  # 山登り法
            model = MountainClimbing(env)
            assert arg1 in [1, 2] and 1 <= arg2 <= 10, "wrong setting"

        # 初期状態から探索
        best_board, best_score = model.search(
            kwargs['executiontime'], arg1, arg2)
        print("最終配列")
        pprint.pprint(best_board)
        print("スコア")
        print(best_score)

    elif kwargs['model'] == '3':  # 盤面の評価のみ
        env = Environment(kwargs['setting'])
        print("評価配列")
        pprint.pprint(env.board)
        print("スコア")
        print(env.score(board2map(env.board), int(kwargs['setting'][1])))

    else:
        print('No model like '+kwargs['model'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument(
        '-m', '--model', type=str, required=True
    )
    parser.add_argument(
        '-t', '--executiontime', type=int
    )
    parser.add_argument(
        '-s', '--setting', type=str, nargs='+',
        help='初期化配列(random,qwerty) スコア種類(1,2) [m=1]温度種類(1,2) [m=2]探索回数(1-10)'
    )
    FLAGS = vars(parser.parse_args())
    main(**FLAGS)
