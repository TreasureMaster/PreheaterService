"""Класс секундомера."""

import time


class StopWatch:

    def __init__(self):
        self.secs = 0
        self.mins = 0
        self.__start = int(time.time())

    def set_elapsed(self):
        diff_time = int(time.time() - self.__start)
        self.mins = int(diff_time/60)
        self.secs = diff_time - self.mins * 60


if __name__ == '__main__':
    sw = StopWatch()
    print(f'Время: {sw.mins} мин {sw.secs} сек')
    for i in range(5):
        time.sleep(1)
        sw.set_elapsed()
        print(f'Время: {sw.mins} мин {sw.secs} сек')