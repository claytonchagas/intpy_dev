#power_recursive.py

import time
import sys

from intpy.intpy import initialize_intpy, deterministic


@deterministic
def pow(n, m):
    if m == 0:
        return 1
    return n*pow(n, m-1)


@initialize_intpy(__file__)
def main(n, m):
    print(pow(n, m))


if __name__ == "__main__":
    n, m = int(sys.argv[1]), int(sys.argv[2])
    start = time.perf_counter()
    main(n, m)
    print(time.perf_counter()-start)
