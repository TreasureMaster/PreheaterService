import time


def sleep(interval):
    start = time.perf_counter()
    while (time.perf_counter() < start + interval):
        pass