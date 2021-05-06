import time

from intpy.intpy import deterministic


@deterministic
def fib(n):
    if n < 2:
        return n

    return fib(n-1) + fib(n-2)


if __name__ == "__main__":
    start = time.perf_counter()
    print(fib(200))
    print(time.perf_counter()-start,"s")