import Environment
import Search1
import argparse
import time


def main(**kwargs):
    env = Environment()
    search = Search1()
    board = kwargs['initial']
    start = time.time()
    now = start
    etime = kwargs['executiontime']
    while(now - start > etime):
        board = search.search()


if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument(
        '-m', '--model', type=str, required=True
    )
    parser.add_argument(
        '-t', '--executiontime', type=int
    )
    FLAGS = vars(parser.parse_args())
    main(**FLAGS)
