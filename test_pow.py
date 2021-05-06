import time


def pow(n, m):
    if m == 0:
        return 1

    return n*pow(n, m-1)


if __name__ == "__main__":
    start = time.perf_counter()
    print(pow(60, 997))
    print(time.perf_counter()-start,"s")