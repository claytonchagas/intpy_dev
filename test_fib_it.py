import time


def fib(n):
    a,b = 0,1
    for i in range(n):
        a,b = b,a+b
    return a


if __name__ == "__main__":
    start = time.perf_counter()
    print(fib(200))
    print(time.perf_counter()-start,"s")