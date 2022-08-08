import random as rnd
import numpy as np
from setup import *

class parameter :

	def __init__(self, Name, minim, maxi, Width):
		self.name = Name
		self.min = float(minim)
		self.max = float(maxi)
		self.width = float(Width)
		self.val = -1e15
		self.prev_val = -1e15
		self.step = float(Width)

	def set_val(self,value):
		self.val = value

	def initialise(self):
		self.set_val(rnd.uniform(self.min,self.max))
		self.prev_val = self.val

	def accepted(self):
		self.prev_val = self.val
		self.step = float(self.width)

	
	def rejected(self):	#diminish the value of the step
		self.step *= Step_decreases




	def jump(self):
		proposal_width = (self.max - self.min) * self.step
		proposal = rnd.gauss(self.prev_val, proposal_width )
		while proposal < self.min or proposal > self.max :							            #ensure that gaussian value is within required range            	
			proposal = rnd.gauss(float(self.prev_val),proposal_width)
		self.val = proposal


