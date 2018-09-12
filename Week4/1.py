from __future__ import print_function
import numpy as np
import random


class Environment:

    def __init__ (self, n):
        self.arr = np.arange(1, n * n + 1).reshape((n, n))
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

    def move_up(self, s):
        v1 = self.zero[0]
        v2 = self.zero[1]
        if v1 == 0:
            return False, s
        else:
            s[v1][v2] = s[v1 - 1][v2]
            s[v1 - 1][v2] = self.n * self.n
            self.zero = v1 - 1, v2
            return True, s

    def move_down(self, s):
        v1 = self.zero[0]
        v2 = self.zero[1]
        if v1 == self.n - 1:
            return False, s
        else:
            s[v1][v2] = s[v1 + 1][v2]
            s[v1 + 1][v2] = self.n * self.n
            self.zero = v1 + 1, v2
            return True, s

    def move_right(self, s):
        v1 = self.zero[0]
        v2 = self.zero[1]
        if v2 == self.n - 1:
            return False, s
        else:
            s[v1][v2] = s[v1][v2 + 1]
            s[v1][v2 + 1] = self.n * self.n
            self.zero = v1, v2 + 1
            return True, s

    def move_left(self, s):
        v1 = self.zero[0]
        v2 = self.zero[1]
        if v2 == 0:
            return False, s
        else:
            s[v1][v2] = s[v1][v2 - 1]
            s[v1][v2 - 1] = self.n * self.n
            self.zero = v1, v2 - 1
            return True, s

    def testing(self, steps):
        for i in range(0, steps):
            j = random.randint(0, 4)
            if j == 0:
                print ("\nmoving up")
                _, self.arr = self.move_up(self.arr)
                print (self.arr)
            if j == 1:
                print ("\nmoving right")
                _, self.arr = self.move_right(self.arr)
                print(self.arr)
            if j == 2:
                print ("\nmoving down")
                _, self.arr = self.move_down(self.arr)
                print(self.arr)
            if j == 3:
                print ("\nmoving left")
                _, self.arr = self.move_left(self.arr)
                print(self.arr)


env = Environment(4)
env.testing(20)


