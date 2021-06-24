import time
import sys
from intpy.intpy import deterministic, initialize_intpy

@deterministic
def heap_permutation(data, n):
    if n == 1:
        #print(data)
        return
    for i in range(n):
        heap_permutation(data, n - 1)
        if n % 2 == 0:
            data[i], data[n - 1] = data[n - 1], data[i]
        else:
            data[0], data[n - 1] = data[n - 1], data[0]


@initialize_intpy(__file__)
def main(n):
    #data = [1, 2, 3, 4, 5, 6]
    #data2 = list(range(8))
    data2 = list(range(n))
    print(data2)
    start_time = time.perf_counter()
    heap_permutation(data2, len(data2))
    end_time = time.perf_counter()
    print(end_time - start_time)

if __name__ == "__main__":
    n = int(sys.argv[1])
    main(n)