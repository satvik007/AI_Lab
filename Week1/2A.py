from __future__ import print_function

"""
The logic behind the program is to move both the sides in increasing number of 
successive steps forming a pattern like    +1 -1 +2 -2 +3 -3 ...
The agent moves until it percepts shore from the environment.

The main idea is to determine the direction in which the agent should move the next
step and that can be found out by considering the pattern that the agent changes
its direction when its total number of moves is of the form n * (n + 1) / 2.
-1 to +2 is considered as 3 moves here. +1 is reached in 1 move, -1 in 3, +2 in 6 moves 
and so on

This condition of n * (n + 1) / 2 can be determined by solving quadratic equation with 
some careful manipulations or more easily by binary search on n.

A unique thing about this code is that you can play the agent step by step or any given 
number of steps you want. It does not run in a single for loop from start to end.
"""

class Agent:
    def __init__ (self):
        self.resp_location = 0 # Agent's location w.r.t his initial position.
        self.alive = True
        self.dir = 1
        self.moves = 0 # Number of moves that agent has walked from beginning.

    def move(self, env):
        if(self.alive):
            self.dir = self.determine_direction()
            self.resp_location = self.resp_location + self.dir
            self.moves += 1
            if(env.percept(self)):
                self.murder()
        else:
            return False

    # determing direction change with binary search.
    def determine_direction(self):
        lo = 0
        hi = 1e6
        ans = 0
        while(lo <= hi):
            mid = (lo + hi) // 2
            v = (mid + 1) * mid / 2
            if(v <= self.moves):
                lo = mid + 1
                ans = max(ans, mid)
            else:
                hi = mid - 1
        ans += 1
        v = (ans + 1) * ans // 2
        v = int(v)

        if(ans % 2 == 1):
            return 1
        else:
            return -1

    def murder(self):
        self.alive = False

class Environment:
    def __init__ (self, _shore_location, _bunny_location): 
        self.shore_location = _shore_location
        self.agent = None
        self.init_location = _bunny_location

    def percept(self, agent):
        location = self.init_location + agent.resp_location
        if(location == self.shore_location):
            return True
        return False
        
    def step(self):
        """Run the environment for one time step."""
        self.agent.move(self)
        self.print_info()
            
    def print_info(self):
        loc = self.init_location + self.agent.resp_location
        print(loc, '\t', self.agent.moves, '\t', self.percept(self.agent), '\t', self.agent.dir, '\t', self.shore_location)

    def run(self, steps=1000):
        """Run the Environment for given number of time steps."""
        for step in range(steps):
            if(self.agent.alive == False):
                return
            self.step()

def start_the_whole_thing(c_env, c_agent):
    c_env.agent = c_agent
    c_env.run()

c_env = Environment(12, 0)
c_agent = Agent()

start_the_whole_thing(c_env, c_agent)