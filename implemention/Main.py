from Environment import Environment
from Model import searchModel1, searchModel2
import argparse


def main(**kwargs):
    env = Environment(kwargs['initial'])
    if(kwargs['model'] == '1'):
        model = searchModel1(env)
    elif(kwargs['model'] == '2'):
        model = searchModel2(env)
    else:
        print('No model like '+kwargs['model'])
    best = model.search(kwargs['executiontime'])
    print(best)


if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument(
        '-m', '--model', type=str, required=True
    )
    parser.add_argument(
        '-t', '--executiontime', type=int
    )
    parser.add_argument(
        '-i', '--initial', type=str,
        help='randomとかで指定'
    )
    FLAGS = vars(parser.parse_args())
    main(**FLAGS)
