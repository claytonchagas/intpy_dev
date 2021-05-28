import time


def pow(n, m):
    if m == 0:
        return 1

    return n*pow(n, m-1)


if __name__ == "__main__":
    n, m = float(sys.argv[1], float(sys.argv[2])
    start = time.perf_counter()
    print(pow(n, m))
    print(time.perf_counter()-start)
