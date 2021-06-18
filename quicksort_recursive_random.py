#quicksort_recursive_random.py

import time
import sys
import numpy as np

from intpy.intpy import initialize_intpy, deterministic


@deterministic
def quicksort(list):
    if len(list) <= 1:
        return list

    pivot = list[0]
    equal = [x for x in list if x == pivot]
    greater = [x for x in list if x > pivot]
    lesser = [x for x in list if x < pivot]

    return quicksort(lesser) + equal + quicksort(greater)


@initialize_intpy(__file__)
def main(unsort_list):
    print(quicksort(unsort_list))


if __name__ == "__main__":
    #enter in the python command line:
    #pytho3 test_quicksort_random.py start(int) stop(int) size(int)
    #list of numbers to sort, ex: 1 10000 1000
    #sort_list = np.random.randint(1, 10000, (1000))
    n1 = int(sys.argv[1])
    n2 = int(sys.argv[2])
    n3 = int(sys.argv[3])
    unsort_list = np.random.randint(n1, n2, n3)
    start = time.perf_counter()
    main(unsort_list)
    print(time.perf_counter()-start)
