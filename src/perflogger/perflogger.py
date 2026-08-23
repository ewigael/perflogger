import inspect
import time

class PerfLogger:
    def __init__(self, name=None, tick_func=time.perf_counter, avgs_step=1):
        self.name = name if name is not None else inspect.currentframe().f_back.f_code.co_name
        self.tick = tick_func
        self.avgs_step = avgs_step
