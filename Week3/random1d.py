from __future__ import print_function
import numpy as np


class Agent1d:
    dx = [-1, 1]

    def __init__(self):
        self.dir = 0
        self.loc = 0
        self.alive = True

    def determine_direction(self):
        self.dir = np.random.randint(0, 2)
        return self.dir

    def move(self, env):

        if self.alive == False:
            return

        self.dir = self.determine_direction()
        per = env.percept(self.dir)

        if per:
            self.loc = self.loc + self.dx[self.dir]

        if per == 2:
            self.alive = False


class Environment1d:
    dx = [-1, 1]

    def __init__(self, l):
        self.agent = Agent1d()
        self.l = l
        m = (l + 1) // 2
        self.iloc = m

    def percept(self, dir):
        nloc = self.iloc + self.agent.loc + self.dx[dir]
        if(nloc == self.l):
            return 2
        if(nloc < 0 or nloc > self.l):
            return 0
        return 1

    def reset(self):
        self.agent = Agent1d()

    def run(self):
        moves = 0
        while self.agent.alive:
            self.agent.move(self)
            moves += 1
        return moves

l = 10
env = Environment1d(l)

k = 1000
moves = 0

for i in range(1, k):
    cm = env.run()
    print (cm)
    moves += cm
    env.reset()

print(moves / k)