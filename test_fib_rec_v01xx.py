import time

from intpy.intpy import deterministic, salvarCache


@deterministic
def fib(n):
    if n < 2:
        return n

    return fib(n-1) + fib(n-2)


if __name__ == "__main__":
    n = float(sys.argv[1])
    start = time.perf_counter()
    print(fib(n))
    #salvarCache()
    print(time.perf_counter()-start)
