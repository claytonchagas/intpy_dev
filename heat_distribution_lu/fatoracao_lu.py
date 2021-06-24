import numpy as np
import sys

#import sys
#sys.path.insert(0, '/home/clayton/Dt/codes/IntPy-experiments-master_EScience_2019/')
from intpy.intpy import deterministic

@deterministic
def fatoracao_lu(A):
    n = len(A)

    # Inicializa matrizes L e U
    L = [[0.0] * n for i in range(n)]
    U = [[0.0] * n for i in range(n)]

    for j in range(n):
        #Diagonal de L igual a 1
        L[j][j] = 1.0

        for i in range(j+1):
            soma = 0
            for k in range(i):
                soma += U[k][j] * L[i][k]
            dense_a_i = np.array(A[i].todense())
            U[i][j] = dense_a_i[0][j] - soma

        for i in range(j, n):
            soma = 0
            for k in range(j):
                soma += U[k][j] * L[i][k]
            dense_a_i = np.array(A[i].todense())
            L[i][j] = (dense_a_i[0][j] - soma) / U[j][j]

    return (L, U)

@deterministic
def resolve_lu(A, B):
    n = len(A)
    L, U = fatoracao_lu(A)

    #Calcula valores de y
    Y_lista = [0 for i in range(n)]
    X_lista = [0 for i in range(n)]

    Y_lista[0] = B[0]
    for l in range(1, n):
        Y_lista[l] = (B[l] - sum(L[l][c] * Y_lista[c] for c in range(n)))/L[l][l]

    X_lista[n-1] = Y_lista[n-1]/U[n-1][n-1]
    for l in reversed(range(0, n-1)):
        X_lista[l] = (Y_lista[l] - sum(U[l][c] * X_lista[c] for c in reversed(range(n))))/U[l][l]

    return X_lista
