from __future__ import print_function
import pickle as pk
import numpy as np 
import queue as Queue

"""
The idea is to use prioriy queue as the data structure and use the given information to 
simulate the traffic system.
When we pop an element out of the priority queue. If the vehicle has not reached last point
we push it back after updating the next time it should pop, the destination it has reached.

Priority queue stores a tuple with priority in the following order.
1. time
2. vehicle_id
3. vehicle_location index

There is a 2D table self.freq which keeps account of number of cars at a given time.

When a car starts at a time. This number is used to calculate its speed. Then with this speed
and distance we calculate the time when this vehicle reaches its next location.

While also popping we also decrement its respective self.freq value for the road it just 
travelled and increment the one it going to travel for calculation of speed for future vehicles
on the same road.

"""

class Environment:
	def __init__ (self):
		self.road = np.array(pk.load(open("road", "rb"), encoding = "latin1"))
		self.time = np.array(pk.load(open("time", "rb"), encoding = "latin1"))
		self.vehicle = np.array(pk.load(open("vehicle", "rb"), encoding = "latin1"))
		self.freq = np.zeros((10, 10), dtype = np.int32) # creates account of the cars on a road.
		self.q = Queue.PriorityQueue()
		self.car_size = self.time.size;
		self.times = np.zeros((self.car_size, 5))

	def print_info(self):
		for i in range(self.car_size):
			for j in range(5):
				print(self.times[i][j] / 60.0, end = ' ');
			print('')
		np.savetxt ("output.csv", self.times, delimiter = ",")

	def calc_speed(self, x):
		return (np.exp(0.5 * x) / (1 + np.exp(0.5 * x)) + 15 / (1 + np.exp(0.5 * x)))

	def run(self):
		q = self.q
		for i in range(self.car_size):
			q.put((self.time[i], i, 0))
			self.times[i][0] = self.time[i]
		
		while q.empty() == False:
			c = q.get()

			u = self.vehicle[c[1]][c[2] - 1]
			v = self.vehicle[c[1]][c[2]]
			self.times[c[1]][c[2]] = c[0]

			if(c[2] != 0):
				self.freq[u][v] -= 1

			if(c[2] == 4):
				continue

			w = self.vehicle[c[1]][c[2] + 1]
		
			cur_speed = self.calc_speed(self.freq[v][w])
			time_taken = self.road[v][w] / cur_speed * 60
			self.freq[v][w] += 1

			q.put((c[0] + time_taken, c[1], c[2] + 1))

env_var = Environment()
env_var.run()
env_var.print_info()
print("A CSV file is also generated.")