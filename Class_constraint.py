

import numpy as np
import math

class Constraint:
	def __init__(self,name, Type, exp_value, sigma):
		self.name = name
		self.exp_val = float(exp_value)
		self.likelihood = -1e15
		self.sigma = float(sigma)
		self.value = -1e15
		self.type = Type
        
	def set_val(self, value):
		self.value = abs(value)
        
    
	def reset_val(self):
		self.value = -1e15
        
                

	def compute_likelihood(self):
		self.likelihood = -1e15
		if self.type == 'G' :
	        	if self.sigma == 0.0 :
	            		print ('ERROR : No sigma given for constraint : ', self.name)
	        	else:
	            		self.likelihood = np.exp(-np.float128(( self.value - self.exp_val)**2/(2*self.sigma **2)) )
	            		
		if self.type == 'S':
			if self.sigma == 0.0 :
	            		print ('ERROR : No sigma given for constraint : ', self.name)
			
			if self.value < self.exp_val:
				self.likelihood = 1.0
			else:
				self.likelihood = np.exp( -np.float128(((self.value) - self.exp_val)**2/(2*self.sigma **2)) )







