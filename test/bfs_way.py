from __future__ import print_function
import numpy as np
import random
import copy
import time

try:
    import queue as Q
except:
    import Queue as Q


class Environment:

    def __init__(self, n, arr):
        self.n = n
        self.arr = arr
        self.final1 = np.arange(1, n * n + 1).reshape((n, n))
        self.final2 = copy.deepcopy(self.final1)
        tx, ty = self.find_zero(self.final2, 0)
        tex, tey = self.find_zero(self.final2, 1)
        self.final2[tx][ty] = self.n * self.n - 1
        self.final2[tex][tey] = self.n * self.n
        self.zero1 = self.find_zero(self.arr, 0)
        self.zero2 = self.find_zero(self.arr, 1)

    def find_zero(self, s, k):
        for i in range(0, self.n):
            for j in range(0, self.n):
                if arr[i][j] == self.n * self.n and k == 0:
                    return i, j
                if arr[i][j] == self.n * self.n - 1 and k == 1:
                    return i, j
        raise EnvironmentError

    def move_up(self, s, zero1, zero2):

        v1 = zero1[0]
        v2 = zero1[1]

        u1 = zero2[0]
        u2 = zero2[1]

        if v1 == 0 or (v1 - 1, v2) == zero2:
            return False, s, zero1, zero2
        else:
            t = s[v1][v2]
            s[v1][v2] = s[v1 - 1][v2]
            s[v1 - 1][v2] = t
            zero1 = v1 - 1, v2
            return True, s, zero1, zero2

    def move_down(self, s, zero1, zero2):
        v1 = zero1[0]
        v2 = zero1[1]

        u1 = zero2[0]
        u2 = zero2[1]

        if v1 == self.n - 1 or (v1 + 1, v2) == zero2:
            return False, s, zero1, zero2
        else:
            t = s[v1][v2]
            s[v1][v2] = s[v1 + 1][v2]
            s[v1 + 1][v2] = t
            zero1 = v1 + 1, v2
            return True, s, zero1, zero2

    def move_right(self, s, zero1, zero2):
        v1 = zero1[0]
        v2 = zero1[1]

        u1 = zero2[0]
        u2 = zero2[1]

        if v2 == self.n - 1 or (v1, v2 + 1) == zero2:
            return False, s, zero1, zero2
        else:
            t = s[v1][v2]
            s[v1][v2] = s[v1][v2 + 1]
            s[v1][v2 + 1] = t
            zero1 = v1, v2 + 1
            return True, s, zero1, zero2

    def move_left(self, s, zero1, zero2):
        v1 = zero1[0]
        v2 = zero1[1]

        u1 = zero2[0]
        u2 = zero2[1]

        if v2 == 0 or (v1, v2 - 1) == zero2:
            return False, s, zero1, zero2
        else:
            t = s[v1][v2]
            s[v1][v2] = s[v1][v2 - 1]
            s[v1][v2 - 1] = t
            zero1 = v1, v2 - 1
            return True, s, zero1, zero2

    def testing(self, steps, can_print=False):
        for i in range(0, steps):
            j = random.randint(0, 4)
            if j == 0:
                if can_print: print("\nmoving up")
                _, self.arr, self.zero1, self.zero2 = self.move_up(self.arr, self.zero1, self.zero2)
                if can_print: print(self.arr)
            if j == 1:
                if can_print: print("\nmoving right")
                _, self.arr, self.zero1, self.zero2 = self.move_right(self.arr, self.zero1, self.zero2)
                if can_print: print(self.arr)
            if j == 2:
                if can_print: print("\nmoving down")
                _, self.arr, self.zero1, self.zero2 = self.move_down(self.arr, self.zero1, self.zero2)
                if can_print: print(self.arr)
            if j == 3:
                if can_print: print("\nmoving left")
                _, self.arr, self.zero1, self.zero2 = self.move_left(self.arr, self.zero1, self.zero2)
                if can_print: print(self.arr)

    def find(self, state, val):
        for i in range(0, self.n):
            for j in range(0, self.n):
                if state[i][j] == val:
                    return i, j

    def h(self, state):
        res = 0
        c = self.find(state, 1)
        res += pow(abs(c[0]) + abs(c[1]), 4)

        if state[0][0] == 1 and state[0][1] == 2:
            res -= 20
        if state[0][0] == 1 and state[1][0] == 5:
            res -= 20
        v1 = state[0][0] == 1 and state[0][1] == 2 and state[0][2] == 3 and state[0][3] == 4
        v2 = state[0][0] == 1 and state[0][1] == 2 and state[0][2] == 3 and state[0][3] == 4 and state[1][0] == 5 and state[1][1] == 6 and state[1][2] == 7 and state[1][3] == 8
        v3 = state[0][0] == 1 and state[1][0] == 5 and state[2][0] == 9 and state[3][0] == 13
        v4 = state[0][0] == 1 and state[1][0] == 5 and state[2][0] == 9 and state[3][0] == 13 and state[0][1] == 2 and state[1][1] == 6 and state[2][1] == 10 and state[3][1] == 14
        if v1:
            res -= 100
        if v2:
            res -= 200
        if v3:
            res -= 100
        if v4:
            res -= 200
        if v1 and v4:
            res -= 1000
        if v3 and v2:
            res -= 1000

        for i in range(0, self.n):
            for j in range(0, self.n):
                val = state[i][j]
                if val >= self.n * self.n - 1:
                    continue
                val -= 1
                x = val // self.n
                y = val % self.n
                res += abs(x - i) + abs(y - j)
        return res

    def call_astar(self):
        ret, parent, depth, final = self.astar()
        print ('\nWe are solving this')
        print (self.arr)
        print ('')
        # print (parent)
        if ret:

            action_seq = []
            state_seq = []
            s = final
            # print(s)
            state_seq.append(final)
            while True:
                _hash = np.array_str(s)
                if parent[_hash][1] == -1:
                    break
                action_seq.append((parent[_hash][1], parent[_hash][2]))
                state_seq.append(parent[_hash][0])
                s = parent[_hash][0]

            action_seq.reverse()
            state_seq.reverse()

            print('Action sequence to be followed\n')
            for i in range(0, len(action_seq)):
                print(state_seq[i])
                x = action_seq[i]
                print (x[1], end = ' ')
                if x[0] == 0:
                    print ('up')
                elif x[0] == 1:
                    print ('right')
                elif x[0] == 2:
                    print ('down')
                elif x[0] == 3:
                    print ('left')

                print ('')

            print (state_seq[len(action_seq)])

            print('\n')

            print('Depth of the tree traversed - ', depth)

        else:
            print('BFS failed to find the goal')

    def astar(self):
        q = Q.PriorityQueue()
        diff = 0
        parent = {}
        dist = {}
        _hash = np.array_str(self.arr)
        parent[_hash] = self.arr, -1, -1
        dist[_hash] = 0

        q.put(((self.h(self.arr), 0, diff), (copy.deepcopy(self.arr), self.zero1, self.zero2)))
        diff += 1
        counter = 0

        while not q.empty():

            f, s = q.get()

            prior, depth, _ = f
            state, zero1, zero2 = s

            if counter % 1000 == 0:
                print (counter, prior, depth, self.h(state))
                print (state)
            counter += 1

            # ((prior, depth), (state, zero)) = q.get()

            if np.array_equal(state, self.final1) or np.array_equal(state, self.final2):
                return True, parent, depth, state

            for i in range(0, 4):

                if i == 0:
                    ret, new_state, new_zero1, new_zero2 = self.move_up(copy.deepcopy(state), zero1, zero2)
                    _hash = np.array_str(new_state)
                    if ret and _hash not in dist or dist[_hash] > depth + 1:
                        parent[_hash] = state, i, zero1
                        dist[_hash] = depth + 1
                        q.put(((self.h(new_state) + depth + 1, depth + 1, diff), (new_state, new_zero1, new_zero2)))
                        diff += 1

                elif i == 1:
                    ret, new_state, new_zero1, new_zero2 = self.move_right(copy.deepcopy(state), zero1, zero2)
                    _hash = np.array_str(new_state)
                    if ret and _hash not in dist or dist[_hash] > depth + 1:
                        parent[_hash] = state, i, zero1
                        dist[_hash] = depth + 1
                        q.put(((self.h(new_state) + depth + 1, depth + 1, diff), (new_state, new_zero1, new_zero2)))
                        diff += 1

                elif i == 2:
                    ret, new_state, new_zero1, new_zero2 = self.move_down(copy.deepcopy(state), zero1, zero2)
                    _hash = np.array_str(new_state)
                    if ret and _hash not in dist or dist[_hash] > depth + 1:
                        parent[_hash] = state, i, zero1
                        dist[_hash] = depth + 1
                        q.put(((self.h(new_state) + depth + 1, depth + 1, diff), (new_state, new_zero1, new_zero2)))
                        diff += 1

                elif i == 3:
                    ret, new_state, new_zero1, new_zero2 = self.move_left(copy.deepcopy(state), zero1, zero2)
                    _hash = np.array_str(new_state)
                    if ret and _hash not in dist or dist[_hash] > depth + 1:
                        parent[_hash] = state, i, zero1
                        dist[_hash] = depth + 1
                        q.put(((self.h(new_state) + depth + 1, depth + 1, diff), (new_state, new_zero1, new_zero2)))
                        diff += 1

            for i in range(0, 4):

                if i == 0:
                    ret, new_state, new_zero1, new_zero2 = self.move_up(copy.deepcopy(state), zero2, zero1)
                    _hash = np.array_str(new_state)
                    if ret and _hash not in dist or dist[_hash] > depth + 1:
                        parent[_hash] = state, i, zero2
                        dist[_hash] = depth + 1
                        q.put(((self.h(new_state) + depth + 1, depth + 1, diff), (new_state, new_zero1, new_zero2)))
                        diff += 1

                elif i == 1:
                    ret, new_state, new_zero1, new_zero2 = self.move_right(copy.deepcopy(state), zero2, zero1)
                    _hash = np.array_str(new_state)
                    if ret and _hash not in dist or dist[_hash] > depth + 1:
                        parent[_hash] = state, i, zero2
                        dist[_hash] = depth + 1
                        q.put(((self.h(new_state) + depth + 1, depth + 1, diff), (new_state, new_zero1, new_zero2)))
                        diff += 1

                elif i == 2:
                    ret, new_state, new_zero1, new_zero2 = self.move_down(copy.deepcopy(state), zero2, zero1)
                    _hash = np.array_str(new_state)
                    if ret and _hash not in dist or dist[_hash] > depth + 1:
                        parent[_hash] = state, i, zero2
                        dist[_hash] = depth + 1
                        q.put(((self.h(new_state) + depth + 1, depth + 1, diff), (new_state, new_zero1, new_zero2)))
                        diff += 1

                elif i == 3:
                    ret, new_state, new_zero1, new_zero2 = self.move_left(copy.deepcopy(state), zero2, zero1)
                    _hash = np.array_str(new_state)
                    if ret and _hash not in dist or dist[_hash] > depth + 1:
                        parent[_hash] = state, i, zero2
                        dist[_hash] = depth + 1
                        q.put(((self.h(new_state) + depth + 1, depth + 1, diff), (new_state, new_zero1, new_zero2)))
                        diff += 1

        return False, None


file_name = 'in.txt'
file = open(file_name)

n = int(file.readline())
arr = np.zeros((n, n))

for i in range(0, n):
    arr[i] = np.array(map(int, file.readline().split()))

print('The following input was read')
print(n)
print(arr)

env = Environment(n, arr)
# env.testing(10)
env.call_astar()
