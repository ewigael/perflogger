import time

from perflogger import PerfLogger

def test_init_default():
    pl = PerfLogger()

    assert pl.name == "test_init_default"
    assert pl.tick == time.perf_counter
    assert pl.avgs_step == 1

def test_init_set():
    pl = PerfLogger(name="perflogger1", tick_func=time.time, avgs_step=10)

    assert pl.name == "perflogger1"
    assert pl.tick == time.time
    assert pl.avgs_step == 10