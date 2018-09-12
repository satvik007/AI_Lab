from __future__ import print_function
import numpy as np

class Agent3d:
    dx = [-1, 1, 0, 0, 0, 0]
    dy = [0, 0, -1, 1, 0, 0]
    dz = [0, 0, 0, 0, -1, 1]

    def __init__(self):
        self.dir = 0
        self.loc = (0, 0, 0)
        self.alive = True

    def determine_direction(self):
        self.dir = np.random.randint(0, 6)
        return self.dir

    def move(self, env):

        if self.alive == False:
            return

        self.dir = self.determine_direction()
        per = env.percept(self.dir)

        if per:
            self.loc = (self.loc[0] + self.dx[self.dir], self.loc[1] + self.dy[self.dir], self.loc[2] + self.dz[self.dir])

        if per == 2:
            self.alive = False


class Environment3d:
    dx = [-1, 1, 0, 0, 0, 0]
    dy = [0, 0, -1, 1, 0, 0]
    dz = [0, 0, 0, 0, -1, 1]

    def __init__(self, l):
        self.agent = Agent3d()
        self.l = l
        m = (l + 1) // 2
        self.iloc = (m, m, m)

    def percept(self, dir):
        nloc = (self.iloc[0] + self.agent.loc[0] + self.dx[dir], self.iloc[1] + self.agent.loc[1] + self.dy[dir],
                     self.iloc[2] + self.agent.loc[2] + self.dz[dir])
        if(nloc == (self.l, self.l, self.l)):
            return 2
        if(nloc[0] < 0 or nloc[1] < 0 or nloc[2] < 0 or nloc[0] > self.l or nloc[1] > self.l or nloc[2] > self.l):
            return 0
        return 1

    def reset(self):
        self.agent = Agent3d()

    def run(self):
        moves = 0
        while self.agent.alive:
            self.agent.move(self)
            moves += 1
        return moves

l = 10
env = Environment3d(l)

k = 100
moves = 0

for i in range(1, k):
    cm = env.run()
    moves += cm
    env.reset()

print(moves / k)
        
    def determine_direction(self):
        self.dir = np.random.rand(0, 6)

class Environment:
    def __init__(self, l):
        self.agent = Agent()
        self.l = l
        
        
    def reset(self):
        self.agent = Agent()


env = Environment()

