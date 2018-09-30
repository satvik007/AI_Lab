from __future__ import print_function
import numpy as np
import queue as Q
import copy


class Environment:

    dx = [-1, 0, 1, 0]
    dy = [0, 1, 0, -1]

    def __init__(self, n, arr):
        self.n = n
        self.arr = arr
        self.zero1 = self.find(self.arr, self.n * self.n - 1)
        self.zero2 = self.find(self.arr, self.n * self.n)

    def find(self, s, val):
        for i in range(0, self.n):
            for j in range(0, self.n):
                if s[i][j] == val:
                    return i, j

    def call_astar(self):
        ret, parent, s = self.astar()

        path = []
        _hash = np.array_str(s)
        path.append((s, -1, -1))

        while parent[_hash][1] != -1:
            path.append(parent[_hash])
            s = parent[_hash]
            _hash = np.array_str(s[0])

        path.reverse()

        print ('Length of the path is ', len(path) - 1)

        for x in path:
            print (x[0])
            i = x[1]
            j = x[2]
            if i == 0:
                print ('Move ', self.n * self.n - 1, end = ', ')
            elif i == 1:
                print ('Move ', self.n * self.n, end = ', ')
            if j == 0:
                print ('Up')
            elif j == 1:
                print ('Right')
            elif j == 2:
                print ('Down')
            elif j == 3:
                print ('Left')
            print ('')

    def h(self, s):
        ans = 0

        for i in range(0, self.n * self.n):
            x = i // self.n
            y = i % self.n
            val = s[x][y]
            if (val >= self.n * self.n - 1):
                continue
            ans += abs(x - (val - 1) // self.n) + abs(y - (val - 1) % self.n)
        return ans

    def bound(self, a, b):
        return a >= 0 and b >= 0 and a < self.n and b < self.n

    def move(self, state, f, s, zero1, zero2):
        if f == 0:
            tx = zero1[0] + self.dx[s]
            ty = zero1[1] + self.dy[s]
            if self.bound(tx, ty) and (tx, ty) != zero2:
                t = state[zero1[0]][zero1[1]]
                state[zero1[0]][zero1[1]] = state[tx][ty]
                state[tx][ty] = t
                zero1 = (tx, ty)
                return True, state, zero1, zero2
        else:
            tx = zero2[0] + self.dx[s]
            ty = zero2[1] + self.dy[s]
            if self.bound(tx, ty) and (tx, ty) != zero1:
                t = state[zero2[0]][zero2[1]]
                state[zero2[0]][zero2[1]] = state[tx][ty]
                state[tx][ty] = t
                zero2 = (tx, ty)
                return True, state, zero1, zero2
        return False, None, None, None

    def solved(self, s):
        for i in range(0, self.n * self.n - 2):
            x = i // self.n
            y = i % self.n
            if s[x][y] != i + 1:
                return False
        return True

    def astar(self):
        q = Q.PriorityQueue()
        q.put((self.h(self.arr), 0, 0, copy.deepcopy(self.arr), self.zero1, self.zero2))
        parent = {}
        dist = {}
        dist[np.array_str(self.arr)] = 0
        parent[np.array_str(self.arr)] = None, -1, -1
        diff = 1
        counter = 0

        while not q.empty():

            prior, g, _, state, zero1, zero2 = q.get()

            if counter % 1000 == 0:
                print (counter, prior, g)
                print (state)
            counter += 1

            if g > 45:
                continue

            if self.solved(state):
                return True, parent, state

            for i in range(0, 2):
                for j in range(0, 4):
                    ret, nstate, nzero1, nzero2 = self.move(copy.deepcopy(state), i, j, zero1, zero2)
                    if ret:
                        _hash = np.array_str(nstate)

                    if ret and (_hash not in dist or dist[_hash] > g + 1):
                        dist[_hash] = g + 1
                        parent[_hash] = state, i, j
                        q.put((self.h(nstate) + g + 1, g + 1, diff, nstate, nzero1, nzero2))
                        diff += 1

        return False, None, None

file_name = 'in.txt'
file = open(file_name)

n = int(file.readline())
arr = np.zeros((n, n))
for i in range(0, n):
    arr[i] = np.array(map(int, file.readline().split()), dtype=np.int32)

env = Environment(n, arr)
env.call_astar()