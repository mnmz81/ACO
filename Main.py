# -*- coding: utf-8 -*-


from ACO import AntforTSP as ACO
import numpy as np
import os
def PrintBorad(n,shortest_path):
    print("Checkerboard pattern:")
    x = np.zeros((n, n), dtype=int)
    # fill with 1 the alternate rows and columns
    i = 0
    for a in shortest_path:
        x[i,a] = 1
        i += 1
    # print the pattern
    np.savetxt("temp.txt", x, fmt="%d")
    for i in range(n):
        for j in range(n):
            print(x[i][j], end=" ")
        print()

if __name__ == "__main__" :
    Niter = 100
    Nant = 200
    n_queens = 64
    ant_colony = ACO(n_queens, Nant, Niter, rho=0.95, alpha=1, beta=8)
    shortest_path = ant_colony.run()
    PrintBorad(n_queens,shortest_path[0])
    print("shortest_path: {}".format(shortest_path))
