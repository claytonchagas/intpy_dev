#test_pow_rec.py

import time
import sys


@deterministic
def pow(n, m):
    if m == 0:
        return 1
    return n*pow(n, m-1)


@initialize_intpy(__file__)
def main(n, m):
    print(pow(n, m))


if __name__ == "__main__":
    n, m = float(sys.argv[1], float(sys.argv[2])
    start = time.perf_counter()
    main(n, m)
    print(time.perf_counter()-start)
