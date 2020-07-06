from Environment import Environment
from Model import searchModel1, searchModel2
import argparse
import pprint


def main(**kwargs):
    env = Environment(kwargs['setting'])
    if(kwargs['model'] == '1'):
        model = searchModel1(env)
    elif(kwargs['model'] == '2'):
        model = searchModel2(env)
    else:
        print('No model like '+kwargs['model'])
        return
    best = model.search(kwargs['executiontime'])
    print("最終配列")
    pprint.pprint(best)


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
        help='h(>=3) w(>=11) mode(=randomとか)で指定'
    )
    FLAGS = vars(parser.parse_args())
    main(**FLAGS)
