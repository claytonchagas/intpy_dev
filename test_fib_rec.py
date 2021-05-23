#test_fib_rec.py

import time
import sys

from intpy.intpy import deterministic, salvarCache


@deterministic
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)


def main(n):
    start = time.perf_counter()
    print(fib(n))
    salvarCache()
    print(time.perf_counter()-start)


if __name__ == "__main__":
    n = float(sys.argv[1])
    main(n)


