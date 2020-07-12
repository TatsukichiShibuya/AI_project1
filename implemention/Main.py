from Environment import Environment
from Model import SimulatedAnnealing, MountainClimbing, A_star
import argparse
import pprint


def main(**kwargs):
    env = Environment(kwargs['setting'])

    if(kwargs['model'] == '1'):
        model = SimulatedAnnealing(env)
    elif(kwargs['model'] == '2'):
        model = MountainClimbing(env)
    elif(kwargs['model'] == '3'):
        model = A_star(env)
    else:
        print('No model like '+kwargs['model'])
        return

    # 初期状態から探索
    best_board, best_score = model.search(kwargs['executiontime'])
    print("最終配列")
    pprint.pprint(best_board)
    print(best_score)


if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument(
        '-m', '--model', type=str, required=True
    )
    parser.add_argument(
        '-t', '--executiontime', type=int
    )
    parser.add_argument(
        '-s', '--setting', type=str, nargs='+',
        help='mode(=randomとか)を指定'
    )
    FLAGS = vars(parser.parse_args())
    main(**FLAGS)
