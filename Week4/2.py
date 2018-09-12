from __future__ import print_function
import numpy as np
import random


class Environment:

    def __init__ (self, n):
        self.arr = (np.random.randint(0, 4, (n, n)) == np.zeros((n, n)))
        self.arr = np.array(self.arr, dtype=np.int32)
        self.start = (0, 0)
        self.goal = (n - 1, n - 1)
        self.n = n
        self.arr[self.goal[0]][self.goal[1]] = 0
        self.arr[self.start[0]][self.start[1]] = 2
        self.loc = self.start

        print (self.arr)

    def move(self, dir):
        if dir == 0:
            if self.loc[0] == 0 or self.arr[self.loc[0] - 1][self.loc[1]] == 1:
                return False
            else:
                self.arr[self.loc[0]][self.loc[1]] = 0
                self.loc = (self.loc[0] - 1, self.loc[1])
                self.arr[self.loc[0]][self.loc[1]] = 2
                return True

        elif dir == 1:
            if self.loc[1] == self.n - 1 or self.arr[self.loc[0]][self.loc[1] + 1] == 1:
                return False
            else:
                self.arr[self.loc[0]][self.loc[1]] = 0
                self.loc = self.loc[0], self.loc[1] + 1
                self.arr[self.loc[0]][self.loc[1]] = 2
                return True

        elif dir == 2:
            if self.loc[0] == self.n - 1 or self.arr[self.loc[0] + 1][self.loc[1]] == 1:
                return False
            else:
                self.arr[self.loc[0]][self.loc[1]] = 0
                self.loc = self.loc[0] + 1, self.loc[1]
                self.arr[self.loc[0]][self.loc[1]] = 2
                return True

        elif dir == 3:
            if self.loc[1] == 0 or self.arr[self.loc[0]][self.loc[1] - 1] == 1:
                return False
            else:
                self.arr[self.loc[0]][self.loc[1]] = 0
                self.loc = self.loc[0], self.loc[1] - 1
                self.arr[self.loc[0]][self.loc[1]] = 2
                return True

        else:
            print ("Direction not defined")
            raise EnvironmentError

    def testing(self, moves):

        for i in range(0, moves):
            dir = random.randint(0, 3)
            if dir == 0:
                print ('\nmoving up')
            elif dir == 1:
                print ('\nmoving right')
            elif dir == 2:
                print ('\nmoving down')
            elif dir == 3:
                print ('\nmoving left')

            self.move(dir)
            print (self.arr)




env = Environment(10)
env.testing(20)

