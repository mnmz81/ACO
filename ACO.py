# -*- coding: utf-8 -*-
import numpy as np
import random

class AntforTSP(object):
    def __init__(self, Nqueen, Nant, Niter, rho, alpha=1, beta=1, seed=None):
        self.Nqueen = Nqueen
        self.conflicts = None
        self.Nant = Nant
        self.Niter = Niter
        self.rho = rho
        self.alpha = alpha
        self.beta = beta
        self.pheromone = np.ones((Nqueen, Nqueen)) / Nqueen
        self.local_state = np.random.RandomState(seed)

    def run(self):
        shortest_path = None
        best_path = ("TBD", np.inf)
        for i in range(self.Niter):
            self.conflicts = np.zeros((self.Nant, self.Nqueen))
            all_paths = self.constructColonyPaths()
            self.depositPheronomes(all_paths)
            shortest_path = min(all_paths, key=lambda x: x[1])
            print(i + 1, ":", shortest_path[1])
            if shortest_path[1] < best_path[1]:
                best_path = shortest_path
            if shortest_path[1] == 0:
                return best_path
            self.pheromone * self.rho  # evaporation
            del self.conflicts
        return best_path

    def depositPheronomes(self, all_paths):
        ant = 0
        for path, _ in all_paths:
            for i in range(self.Nqueen):
                self.pheromone[path[i]][i] += 1.0/(self.conflicts[ant][i]+1)
            ant += 1

    def evalTour(self, ant):
        return np.mod(sum(self.conflicts[ant]), self.Nqueen)

    def constructColonyPaths(self):
        all_path = []
        for ant in range(self.Nant):
            path = []
            for queen in range(self.Nqueen):
                path = self.nextMove(queen, path, ant)
            all_path.append((path, self.evalTour(ant)))
        return all_path

    def nextMove(self, queen, path, ant):
        pheromone = np.copy(self.pheromone[:][queen])
        penalty_cnt = self.penalty_counter(path)
        row = pheromone ** self.alpha * ((1 / penalty_cnt) ** self.beta)
        move = random.choices(population=range(self.Nqueen), weights=row)[0]
        path.append(move)
        self.conflicts_update(ant, path, penalty_cnt)
        return path

    def penalty_counter(self, path):
        path_len = len(path)
        penalties = np.ones(self.Nqueen)
        for row in range(self.Nqueen):
            for queen in range(path_len):
                if path[queen] == row or path_len + row == queen + path[queen] or path_len - row == queen - path[queen]:
                    penalties[row] += 1
        return penalties

    def conflicts_update(self, ant, path, cnt):
        last_index = len(path) - 1
        if cnt[path[last_index]] != 0:
            self.conflicts[ant][last_index] += 1
        for queen in range(last_index):
            if path[queen] == path[last_index] or path[queen] + queen == path[last_index] + last_index or \
                    path[queen] - queen == path[last_index] - last_index:
                self.conflicts[ant][queen] += 1
