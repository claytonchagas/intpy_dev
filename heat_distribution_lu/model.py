import numpy as np

class Model:

    def __init__(self, nx, ny, dimensionality):
        self.shape = (int(dimensionality[0]/nx), int(dimensionality[1]/ny))
        self.nx = nx
        self.ny = ny
        self.initial_distribution = self.get_initial_distribution()

    def get_initial_distribution(self):
        matrix = np.zeros(self.shape)

        #Calculate Vertical Boundaries
        for x in [0, len(matrix)-1]:
            for y in range(len(matrix[x])):
                matrix[x][y] = self.u(x*self.nx, y*self.ny)

        #Calculate Horizontal Boundaries
        for y in [0, len(matrix[0])-1]:
            for x in range(len(matrix)):
                matrix[x][y] = self.u(x*self.nx, y*self.ny)

        return matrix

    def u(self, x , y):
        return 2*x + y**2

