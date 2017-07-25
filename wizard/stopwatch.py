import time

class Stopwatch(object):
    def __init__(self):
        self.last_time = time.time()

    def tic(self):
        self.last_time = time.time()

    def toc(self, message="", raw=False):
        elapsed = time.time() - self.last_time
        if raw:
            return elapsed
        else:
            print("[{:0.3f} seconds] {}".format(elapsed, message))

    def tictoc(self, message="", raw=False):
        self.toc(message, raw)
        self.tic()

stopwatch = Stopwatch()
