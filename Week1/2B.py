from __future__ import print_function

"""
The program is similar to the previous one. The few main differences are

coordinates are 2D.
To determine whether shore is reached we need equation of line and the property that 
    2 points on differnt sides of a line give values of opposites sign.
We just move along the coordinate axes in the following way.

                3
                2
                1
    -3  -2  -1  0   1   2   3
                -1
                -2
                -3

                3
                2
                1
    -3  -2  -1  0  ->   ->  ->
                -1
                -2
                -3

                3
                2
                1
    -3  -2  -1  0   <-  <-  <-
                -1
                -2
                -3

We go in the following order - Right, down, left, and up successively.
Everytime we go into the same branch we go one coordinate farther than the last time.

Again the agent can be asked to run for any number of desired steps. This is indeed the 
way recommended on the AIMA Github file - agents.py
"""

class pair:
    def __init__ (self, x = 0, y = 0):
        self.x = x
        self.y = y
    
    def add(self, a):
        return pair(self.x + a.x, self.y + a.y)
    
    def equals(self, a):
        return (self.x == a.x and self.y == a.y)

class Agent:
    # variables help in moving. They are in clockwise manner.
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]

    def __init__ (self):
        self.current = pair(0, 0)
        self.dir = 1
        self.moves = 0
        self.alive = True
        self.energy = 1 # Determines when to change direction and when not to.
        self.potential = 1 # This is given to the var self.energy.

    def move(self, env):
        if(self.alive == False):
            return
        self.dir = self.determine_direction()
        self.current.x += self.dr[self.dir]
        self.current.y += self.dc[self.dir]
        self.energy -= 1
        self.moves += 1
        if(env.percept()):
            self.alive = False

    def determine_direction(self):
        if self.energy == 0:
            if self.current.x == 0 and self.current.y == 0:
                if self.dir == 0:
                    self.potential += 1
                self.dir = (self.dir + 1) % 4 # moving clockwise.
            else:
                self.dir = (self.dir + 2) % 4 # moving opposite direction.
            self.energy += self.potential

        return self.dir
        

class Environment:
    def __init__ (self, loc_agent, a, b, c): 
        self.agent = Agent()
        self.loc_agent = loc_agent
        self.a = a
        self.b = b
        self.c = c
        self.sign = self.line_sign(self.loc_agent)

    def line_sign(self, p):
        v = (self.a * p.x + self.b * p.y + self.c)
        if v > 0: 
            return 1
        elif v == 0: 
            return 0
        else: 
            return -1

    def percept(self):
        loc = self.agent.current.add(self.loc_agent)
        return (self.line_sign(loc) == 0 or self.line_sign(loc) * self.sign < 0)

    def step(self):
        """Run the environment for one time step."""
        self.agent.move(self)
        self.print_info()
               
    def print_info(self):
        loc = self.agent.current.add(self.loc_agent)
        print("(" + str(loc.x) + ", " + str(loc.y) + ")")

    def run(self, steps=1000):
        """Run the Environment for given number of time steps."""
        for step in range(steps):
            if(self.agent.alive == False):
                return
            self.step()

def start_the_whole_thing():
    loc_agent = pair(0, 0)
    (a, b, c) = (1, 1, -5) # shore is along the line    x + y = 5
    var_env = Environment(loc_agent, a, b, c)
    var_env.run()

start_the_whole_thing()