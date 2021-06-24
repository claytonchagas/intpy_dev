from solver import Solver
from model import Model

#absolute path:
#pythonic mode:
#import sys
#sys.path.insert(0, '/home/clayton/Dt/codes/IntPy-experiments-master_EScience_2019/')
#4Lnx mode: export PYTHONPATH='/home/clayton/Dt/codes/IntPy-experiments-master_EScience_2019/'
#4Win mode: SET PYTHONPATH='path/to/directory'
#echo $PYTHONPATH

from intpy.intpy import initialize_intpy
import time

@initialize_intpy(__file__)
def main():
    dimensionality = (2,2)
    nx = 0.15
    ny = 0.15
    delta_t = 0.1
    start_time = time.time()
    model = Model(nx, ny, dimensionality)
    solver = Solver(model, delta_t)
    solver.solve()
    end_time = time.time()
    print(end_time - start_time)

if __name__ == "__main__":
    main()
