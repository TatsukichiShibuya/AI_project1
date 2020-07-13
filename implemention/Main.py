from Environment import Environment
from Model import SimulatedAnnealing, MountainClimbing, board2map
import argparse
import pprint


def main(**kwargs):

    if kwargs['model'] in ['1', '2']:  # search
        env = Environment(kwargs['setting'][0])
        arg = int(kwargs['setting'][1])

        if kwargs['model'] == '1':  # SimulatedAnnealing
            model = SimulatedAnnealing(env)
            assert arg in [1, 2], "wrong setting"
        elif kwargs['model'] == '2':  # MountainClimbing
            model = MountainClimbing(env)
            assert 1 <= arg <= 20, "wrong setting"

        # execute search
        best_board, best_score = model.search(
            kwargs['executiontime'], arg)
        print("Final Board")
        pprint.pprint(best_board)
        print("Score")
        print(best_score)

    elif kwargs['model'] == '3':  # only evaluate board
        env = Environment(kwargs['setting'][0])
        print("Borad to Evaluate")
        pprint.pprint(env.board)
        print("Score")
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
        help='初期配列(random or qwerty) [if m=1]温度種類(1 or 2) [if m=2]探索回数(1-20)'
    )
    FLAGS = vars(parser.parse_args())
    main(**FLAGS)
