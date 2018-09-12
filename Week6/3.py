from __future__ import print_function
import numpy as np
import random
import queue as Q
import time

class Environment:

    def __init__ (self, n):
        self.arr = (np.random.randint(0, 4, (n, n)) == np.zeros((n, n)))
        self.arr = np.array(self.arr, dtype=np.int32)
        self.start = (0, 0)
        self.goal = (n - 1, n - 1)
        self.n = n
        self.arr[self.goal[0]][self.goal[1]] = 0
        self.arr[self.start[0]][self.start[1]] = 0
        self.loc = self.start
        print (self.arr)

    def move(self, pos, dir):
        if dir == 0:
            if pos[0] == 0 or self.arr[pos[0] - 1][pos[1]] == 1:
                return False, pos
            else:
                pos = (pos[0] - 1, pos[1])
                return True, pos

        elif dir == 1:
            if pos[1] == self.n - 1 or self.arr[pos[0]][pos[1] + 1] == 1:
                return False, pos
            else:
                pos = pos[0], pos[1] + 1
                return True, pos

        elif dir == 2:
            if pos[0] == self.n - 1 or self.arr[pos[0] + 1][pos[1]] == 1:
                return False, pos
            else:
                pos = pos[0] + 1, pos[1]
                return True, pos

        elif dir == 3:
            if pos[1] == 0 or self.arr[pos[0]][pos[1] - 1] == 1:
                return False, pos
            else:
                pos = pos[0], pos[1] - 1
                return True, pos

        else:
            print ("Direction not defined")
            raise EnvironmentError

    def testing(self, moves, should_print = False):

        for i in range(0, moves):
            dir = random.randint(0, 3)
            ret, self.loc = self.move(self.loc, dir)

            if should_print:
                if dir == 0:
                    print('\nmoving up')
                elif dir == 1:
                    print('\nmoving right')
                elif dir == 2:
                    print('\nmoving down')
                elif dir == 3:
                    print('\nmoving left')
                print(self.arr)

    def h(self, state):
        return abs(state[0] - self.goal[0]) + abs(state[1] - self.goal[1])

    def call_astar(self):

        ret, parent = self.astar()

        if ret:
            s = self.goal
            path = []

            while s in parent:
                path.append(s)
                s = parent[s]

            path.reverse()
            print ("\nThe bot should follow this path")
            print(path)
            return True

        else:
            print ('Target not found')

    def astar(self):

        q = Q.PriorityQueue()
        q.put((self.h(self.start), 0, self.start))
        parent = {}
        parent[self.start] = (-1, -1)
        dist = {}
        dist[self.start] = 0

        while not q.empty():

            _, g, state = q.get()

            if state == self.goal:
                return True, parent

            for i in range(0, 4):
                ret, new_state = self.move(state, i)
                if ret and new_state not in dist or dist[new_state] > g + 1:
                    parent[new_state] = state
                    dist[new_state] = g + 1
                    q.put((self.h(new_state) + g + 1, g + 1, new_state))

        return False, None


env = Environment(10)
# env.testing(20, True)
env.call_astar()

