#fibonacci_iterative.py

import time
import sys

from intpy.intpy import initialize_intpy, deterministic


@deterministic
def fib(n):
    a,b = 0,1
    for i in range(n):
        a,b = b,a+b
    return a


@initialize_intpy(__file__)
def main(n):
    print(fib(n))


if __name__ == "__main__":
    n = int(sys.argv[1])
    start = time.perf_counter()
    main(n)
    print(time.perf_counter()-start)
