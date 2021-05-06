import time
import random
import numpy as np

from intpy import deterministic


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
    
    sort_list2 = np.random.randint(1, 10000, (1000))
    sort_list = [1, 2, 5, 2, 1, 0, 199, 2, 3]
    print(sort_list2)
    start = time.perf_counter()
    print(quicksort(sort_list2))
    print(time.perf_counter()-start,"s")