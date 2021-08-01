import functools, time


def timethis(func=None, *, num_iter=1):
    # со скобками, т.е. исполняется в коде
    if func is None:
        return lambda func: timethis(func, num_iter=num_iter)

    @functools.wraps(func)
    def inner(*args, **kwargs):
        print(func.__name__, end=' ... \n')
        acc = float('inf')
        for i in range(num_iter):
            tick = time.perf_counter()
            result = func(*args, **kwargs)
            # выбирает минимальное значение из всех прогонов функции
            acc = min(acc, time.perf_counter() - tick)
        print(acc)
        return result
    return inner


if __name__ == '__main__':
    result = timethis(sum)(range(10 ** 6))
    result = timethis(sum, num_iter=100)(range(10 ** 6))