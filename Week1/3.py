from __future__ import print_function

"""
The main idea is to move in a spiral.
The main thing different in this program from 2B is the determine_direction() function.
This time it is implemented considering the pattern that we have to turn clockwise when
the number of moves from the start become of the order of  n * (n - 1) or n * n.
This time we did it with solving quadratic equation rather than binay search as in 2A.
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
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]

    def __init__ (self):
        self.current = pair(0, 0)
        self.dir = 1
        self.moves = 0
        self.alive = True

    def move(self, env):
        if(self.alive == False):
            return
        self.dir = self.determine_direction()
        self.current.x += self.dr[self.dir]
        self.current.y += self.dc[self.dir]
        self.moves += 1
        if(env.percept()):
            self.alive = False 

    def determine_direction(self):
        """ Possibly the toughest function"""
        k = self.moves
        a = int((1 + (1 + 4 * k) ** (0.5)) // 2)
        b = int(k ** (0.5))
        if(a * (a - 1) == k or b * b == k):
            self.dir = (self.dir + 1) % 4
        return self.dir
        # raise NotImplementedError

class Environment:
    def __init__ (self, loc_dirt, loc_agent): 
        self.agent = Agent()
        self.loc_agent = loc_agent
        self.loc_dirt = loc_dirt

    def percept(self):
        loc = self.agent.current.add(self.loc_agent)
        return (loc.equals(self.loc_dirt))

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
    loc_dirt = pair(3, 3)
    loc_agent = pair(0, 0)
    var_env = Environment(loc_dirt, loc_agent)
    var_env.run()

start_the_whole_thing()