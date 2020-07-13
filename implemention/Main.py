from Environment import Environment
from Model import SimulatedAnnealing, MountainClimbing, board2map
import argparse
import pprint


def main(**kwargs):

    if kwargs['model'] in ['1', '2']:  # 探索
        env = Environment(kwargs['setting'][0])
        arg = int(kwargs['setting'][1])

        if kwargs['model'] == '1':  # 焼き鈍し法
            model = SimulatedAnnealing(env)
            assert arg in [1, 2], "wrong setting"
        elif kwargs['model'] == '2':  # 山登り法
            model = MountainClimbing(env)
            assert 1 <= arg <= 10, "wrong setting"

        # 初期状態から探索
        best_board, best_score = model.search(
            kwargs['executiontime'], arg)
        print("最終配列")
        pprint.pprint(best_board)
        print("スコア")
        print(best_score)

    elif kwargs['model'] == '3':  # 盤面の評価のみ
        env = Environment(kwargs['setting'][0])
        print("評価配列")
        pprint.pprint(env.board)
        print("スコア")
        print(env.score(board2map(env.board)))

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
        help='初期化配列(random,qwerty) [m=1]温度種類(1,2) [m=2]探索回数(1-10)'
    )
    FLAGS = vars(parser.parse_args())
    main(**FLAGS)
