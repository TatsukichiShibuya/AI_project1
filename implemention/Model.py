import time


class searchModel1:
    def __init__(self, env):
        self.env = env

    def search(self, executiontime):
        etime = executiontime*1000
        start = time.time()
        now = start
        while(now-start > etime):
            now = time.time()
        best = self.env.board
        return best


class searchModel2:
    def __init__(self):
        pass

    def search(self):
        pass
