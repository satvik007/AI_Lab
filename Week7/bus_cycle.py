from __future__ import print_function

import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import copy
import xlrd

try:
    import queue as Q
except:
    import Queue as Q


np.set_printoptions(threshold=np.inf)


class Environment:

    def __init__ (self, congest, budget, cost, n):

        self.v1 = 25 # cycle speed
        if congest == 0:
            self.v2 = 50
        elif congest == 1:
            self.v2 = 37.5
        elif congest == 2:
            self.v2 = 10 # bus speed

        self.budget = budget
        self.cost = cost
        self.n = n
        self.read_files()
        self.start = 0
        self.goal = 13

    def read_files(self):
        self.dist = np.zeros((self.n, self.n))
        self.nodes = range(0, self.n)
        dist_file_name = 'dist.txt'
        nodes_file_name = 'nodes.txt'

        dist_file = open(dist_file_name)
        for i in range(0, self.n):
            current_line = dist_file.readline()
            tokens = current_line.split()
            for j in range(0, self.n):
                if tokens[j] == 'N':
                    self.dist[i][j] = -1
                else:
                    self.dist[i][j] = float (tokens[j])

        nodes_file = open(nodes_file_name)
        for i in range(0, self.n):
            current_line = nodes_file.readline()
            _, x, y = map(int, current_line.split())
            self.nodes[i] = (x, y)

    def h(self, s):
        goal = self.nodes[self.goal]
        v = max(self.v1, self.v2)
        return (np.hypot(s[0] - goal[0], s[1] - goal[1]) / v)

    def astar(self):

        pq = Q.PriorityQueue()
        # (g + h, g, state, cost)
        pq.put((self.h(self.nodes[self.start]), 0, 0, 0))
        parent = {}
        parent[(0, 0, 0)] = None

        while not pq.empty():

            _, g, state, cost = item = pq.get()

            if cost > self.budget:
                continue

            if state == self.goal:
                return True, parent, item

            for i in range(0, self.n):
                if self.dist[state][i] > 0:
                    if self.dist[state][i] > 3:
                        time = self.dist[state][i] / self.v2
                        parent[(g + time, i, cost + self.cost * time)] = (g, state, cost, 2)
                        pq.put((g + time + self.h(self.nodes[i]), g + time, i, cost + self.cost * time))

                    parent[(g + self.dist[state][i] / self.v1, i, cost)] = (g, state, cost, 1)
                    pq.put((g + self.dist[state][i] / self.v1 + self.h(self.nodes[i]),
                            g + self.dist[state][i] / self.v1, i, cost))

        return False, None, None

    def run(self):
        ret, parent, item = self.astar()
        if ret:
            print ('Total cost = ', item[3], 'Total time = ', item[1])
            path = []
            s = (item[1], item[2], item[3])
            path.append((self.nodes[self.goal], -1))
            while parent[s] != None:
                v = parent[s]
                path.append((self.nodes[v[1]], v[3]))
                s = (v[0], v[1], v[2])

            path.reverse()

            for x in path:
                w = ''
                if x[1] == 1:
                    w = 'cycle'
                elif x[1] == 2:
                    w = 'bus'
                print (x[0], w)

        else:
            print ('Didn\'t quite reach there')

print ('In a tuple 1st val is for state, 2nd is for mode of transport chosen. 1 - cycle, 2 - bus')

print ('\n0% congestion')
env = Environment(0, 10000, 10, 17)
env.run()

print ('\n50% congestion')
env = Environment(1, 10000, 10, 17)
env.run()

print ('\n100% congestion')
env = Environment(2, 10000, 10, 17)
env.run()
