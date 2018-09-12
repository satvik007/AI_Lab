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

    def call_bfs(self):

        ret, parent = self.bfs()

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

    def bfs(self):

        q = Q.Queue()
        q.put(self.start)
        parent = {}
        parent[self.start] = (-1, -1)

        while not q.empty():

            state = q.get()

            if state == self.goal:
                return True, parent

            for i in range(0, 4):
                ret, new_state = self.move(state, i)
                if ret and new_state not in parent:
                    parent[new_state] = state
                    q.put(new_state)

        return False, None


env = Environment(10)
# env.testing(20, True)
env.call_bfs()

