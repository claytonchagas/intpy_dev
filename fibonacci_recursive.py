#fibonacci_recursive.py

import time
import sys

from intpy.intpy import initialize_intpy, deterministic


@deterministic
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)


@initialize_intpy(__file__)
def main(n):
    print(fib(n))


if __name__ == "__main__":
    n = int(sys.argv[1])
    start = time.perf_counter()
    main(n)
    print(time.perf_counter()-start)
