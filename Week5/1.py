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

    def __init__ (self, n):
        self.arr = np.arange(1, n * n + 1).reshape((n, n))
        self.final = copy.deepcopy(self.arr)
        print ('Original array')
        print (self.arr)
        self. n = n
        self.zero = self.find_zero()

    def find_zero(self):
        for i in range(0, self.n):
            for j in range(0, self.n):
                if(self.arr[i][j] == self.n * self.n):
                    return i, j
        raise EnvironmentError

    def d(self, s):
        return abs(self.n - s[0] - 1) + abs(self.n - s[1] - 1)

    def parity(self):
        res = 0
        for i in range(0, self.n * self.n):
            for j in range(i + 1, self.n * self.n):
                x1 = i // self.n
                y1 = i % self.n
                x2 = j // self.n
                y2 = j % self.n

                if self.arr[x2][y2] < self.arr[x1][y1]:
                    res += 1

        return (res + self.d(self.zero)) % 2

    def move_up(self, s, zero):
        v1 = zero[0]
        v2 = zero[1]
        if v1 == 0:
            return False, s, zero
        else:
            s[v1][v2] = s[v1 - 1][v2]
            s[v1 - 1][v2] = self.n * self.n
            zero = v1 - 1, v2
            return True, s, zero

    def move_down(self, s, zero):
        v1 = zero[0]
        v2 = zero[1]
        if v1 == self.n - 1:
            return False, s, zero
        else:
            s[v1][v2] = s[v1 + 1][v2]
            s[v1 + 1][v2] = self.n * self.n
            zero = v1 + 1, v2
            return True, s, zero

    def move_right(self, s, zero):
        v1 = zero[0]
        v2 = zero[1]
        if v2 == self.n - 1:
            return False, s, zero
        else:
            s[v1][v2] = s[v1][v2 + 1]
            s[v1][v2 + 1] = self.n * self.n
            zero = v1, v2 + 1
            return True, s, zero

    def move_left(self, s, zero):
        v1 = zero[0]
        v2 = zero[1]
        if v2 == 0:
            return False, s, zero
        else:
            s[v1][v2] = s[v1][v2 - 1]
            s[v1][v2 - 1] = self.n * self.n
            zero = v1, v2 - 1
            return True, s, zero

    def testing(self, steps, can_print = False):
        for i in range(0, steps):
            j = random.randint(0, 4)
            if j == 0:
                if can_print: print ("\nmoving up")
                _, self.arr, self.zero = self.move_up(self.arr, self.zero)
                if can_print: print (self.arr)
            if j == 1:
                if can_print: print ("\nmoving right")
                _, self.arr, self.zero = self.move_right(self.arr, self.zero)
                if can_print: print(self.arr)
            if j == 2:
                if can_print: print ("\nmoving down")
                _, self.arr, self.zero = self.move_down(self.arr, self.zero)
                if can_print: print(self.arr)
            if j == 3:
                if can_print: print ("\nmoving left")
                _, self.arr, self.zero = self.move_left(self.arr, self.zero)
                if can_print: print(self.arr)

    def call_dfs(self):
        depth = 1
        while True:
            ret, parent = self.dfs(depth)
            if ret:
                print (depth)
                action_seq = []
                state_seq = []
                s = self.final
                state_seq.append(self.final)
                while True:
                    _hash = np.array_str(s)
                    if parent[_hash][1] == -1:
                        break
                    action_seq.append(parent[_hash][1])
                    state_seq.append(parent[_hash][0])
                    s = parent[_hash][0]

                action_seq.reverse()
                state_seq.reverse()

                print('Action sequence to be followed')
                print (action_seq, '\n')

                print('States as they appear while solving')
                for i in state_seq:
                    print (i)

                break

            depth += 1

    def dfs(self, max_depth):
        q = Q.LifoQueue()
        q.put((0, copy.deepcopy(self.arr), self.zero))
        parent = {}
        _hash = np.array_str(self.arr)
        parent[_hash] = self.arr, -1

        while not q.empty():
            depth, state, zero = q.get()

            if depth > max_depth:
                continue

            if np.array_equal(state, self.final):
                return True, parent

            for i in range(0, 4):

                if i == 0:
                    ret, new_state, new_zero = self.move_up(copy.deepcopy(state), zero)
                    _hash = np.array_str(new_state)
                    if ret and _hash not in parent:
                        parent[_hash] = state, 0
                        q.put((depth + 1, new_state, new_zero))

                elif i == 1:
                    ret, new_state, new_zero = self.move_right(copy.deepcopy(state), zero)
                    _hash = np.array_str(new_state)
                    if ret and _hash not in parent:
                        parent[_hash] = state, 1
                        q.put((depth + 1, new_state, new_zero))

                elif i == 2:
                    ret, new_state, new_zero = self.move_down(copy.deepcopy(state), zero)
                    _hash = np.array_str(new_state)
                    if ret and _hash not in parent:
                        parent[_hash] = state, 2
                        q.put((depth + 1, new_state, new_zero))

                elif i == 3:
                    ret, new_state, new_zero = self.move_left(copy.deepcopy(state), zero)
                    _hash = np.array_str(new_state)
                    if ret and _hash not in parent:
                        parent[_hash] = state, 3
                        q.put((depth + 1, new_state, new_zero))

        return False, None


env = Environment(4)
env.testing(10)
print ('Final puzzle to be solved.')
print (env.arr)
env.call_dfs()
