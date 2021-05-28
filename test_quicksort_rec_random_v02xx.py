#test_quicksort_rec_random.py

import time
import random
import numpy as np
#import os
#import sys
#currentdir = os.path.dirname(os.path.realpath(__file__))
#parentdir = os.path.dirname(currentdir)
#sys.path.append(parentdir)
#sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from intpy.intpy import deterministic


@deterministic
def quicksort(list):
    if len(list) <= 1:
        return list

    pivot = list[0]
    equal = [x for x in list if x == pivot]
    greater = [x for x in list if x > pivot]
    lesser = [x for x in list if x < pivot]

    return quicksort(lesser) + equal + quicksort(greater)


if __name__ == "__main__":
    #enter in the python command line:
    #pytho3 test_quicksort_random.py start(int) stop(int) size(int)
    #list of numbers to sort, ex: 1 10000 1000
    #sort_list = np.random.randint(1, 10000, (1000))
    n1 = int(sys.argv[1])
    n2 = int(sys.argv[2])
    n3 = int(sys.argv[3])
    sort_list = np.random.randint(n1, n2, (n3))
    print(sort_list)
    start = time.perf_counter()
    print(quicksort(sort_list))
    salvarCache()
    print(time.perf_counter()-start)
