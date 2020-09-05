"""
This document for benchmark functions is provided by supervisor
"""

import math
import numpy as np
from . import functions_info_loader as fil

functions_info = fil.FunctionsInfo()

class BenchmarkFunction(object):
	def __init__(self, name, n_dimensions=2, opposite=False):
		self.name=name
		self.opposite=opposite
		self.n_dimensions=n_dimensions
		self.parameters=[]

	def __call__(self, point, validate=True):
		if validate:
			self._validate_point(point)
		if self.opposite:
			return - self._evaluate(point)
		else:
			return self._evaluate(point)
	
	def derivative(self, point, validate=True):
		if validate:
			self._validate_point(point)
		if self.opposite:
			return - self._evaluate_derivative(point)
		else:
			return self._evaluate_derivative(point)
	
	def second_derivative(self, point, validate=True):
		if validate:
			self._validate_point(point)
		if self.opposite:
			return - self._evaluate_second_derivative(point)
		else:
			return self._evaluate_second_derivative(point)

	def _validate_point(self, point):
		if type(point)!=tuple and type(point)!=list:
			raise ValueError("Functions can be evaluated only on tuple or lists of values, found "+str(type(point)))
		if len(point)!=self.n_dimensions:
			raise ValueError("Function "+self.name+" declared as defined for "+str(self.n_dimensions)+" dimensions, asked to be evaluated on a point of "+str(len(point))+" dimensions")
		if not all(type(v)==float or type(v)==int or type(v)==np.float64 for v in point):
			idx=None
			for i in range(len(point)):
				t=type(point[i])
				if t!=float and t!=int:
					idx=i
					break
			vs=[x for x in point]
			vs[idx]=str(vs[idx])+"("+str(type(vs[idx]))+")"
			raise ValueError("Functions can only be evaluated on float or int values, passed "+str(vs))
	
	def _evaluate(self, point):
		raise NotImplementedError("Function "+self.name+" is not defined.")
	def _evaluate_derivative(self, point):
		raise NotImplementedError("Derivative of function "+self.name+" is not defined.")
	def _evaluate_second_derivative(self, point):
		raise NotImplementedError("Second derivative of function "+self.name+" is not defined.")
	
	def getName(self):
		return self.name

	def getMinima(self):
		if self.opposite:
			return [(self(v), v) for v in functions_info.get_maxima(self.name, self.n_dimensions, self.parameters)]
		else:
			return [(self(v), v) for v in functions_info.get_minima(self.name, self.n_dimensions, self.parameters)]
	# return a tuple (value, position)
	def getMinimum(self):
		minima = self.getMinima()
		if len(minima)==0:
			return None
		pos=0
		for i in range(len(minima))[1:]:
			if minima[i][0]<minima[pos][0]:
				pos=i
		return minima[pos]

	def getMaxima(self):
		if self.opposite:
			return [(self(v), v) for v in functions_info.get_minima(self.name, self.n_dimensions, self.parameters)]
		else:
			return [(self(v), v) for v in functions_info.get_maxima(self.name, self.n_dimensions, self.parameters)]
	# return a tuple (value, position)
	def getMaximum(self):
		maxima = self.getMaxima()
		if len(maxima)==0:
			return None
		pos=0
		for i in range(len(maxima))[1:]:
			if maxima[i][0]>maxima[pos][0]:
				pos=i
		return maxima[pos]

	def getSuggestedBounds(self):
		b=functions_info.get_suggested_bounds(self.name, self.parameters)
		return ([b[0]]*self.n_dimensions, [b[1]]*self.n_dimensions)

'''
Continuous, non-convex and multimodal.
Clear global minimum at the center surrounded by many symmetrical local minima.
'''
class Ackley(BenchmarkFunction):
	def __init__(self, n_dimensions=2,a=20,	b=.2,	c=2.0*math.pi, opposite=False):
		super().__init__("Ackley", n_dimensions, opposite)
		self.a=a
		self.b=b
		self.c=c
	def _evaluate(self,point):
		part1=0.0
		part2=0.0
		for i in range(len(point)):
			part1+=pow(point[i],2)
			part2+=math.cos(self.c*point[i])
		ret = -self.a * math.exp(-self.b * math.sqrt(part1/len(point))) - math.exp(part2/len(point)) + self.a + math.exp(1.0)	
		return ret

class Schaffer(BenchmarkFunction):
	def __init__(self, opposite=False):
		super().__init__("Schaffer", 2, opposite)
	def _evaluate(self,point):
		tmp=pow(point[0],2) + pow(point[1],2)
		ret = 0.5 + (pow(math.sin(math.sqrt(tmp)),2) - 0.5)/pow(1.0 + 0.001*tmp,2)
		return ret

'''
Continuous, non-convex and (highly) multimodal. 
Location of the minima are geometrical distant.
'''
class Schwefel(BenchmarkFunction):
	def __init__(self, n_dimensions=2, opposite=False):
		super().__init__("Schwefel", n_dimensions, opposite)
	def _evaluate(self,point):
		ret = sum([-p*math.sin(math.sqrt(abs(p))) for p in point])
		return ret
	def _evaluate_derivative(self, point):
		if point==[0.0]*len(point):
			return 0.0
		else:
			return sum([-pow(p,2)*math.cos(math.sqrt(abs(p)))/(2.0*pow(abs(p),3.0/2.0)) - math.sin(math.sqrt(abs(p))) for p in point if p!=0.0])

'''
Continuous, unimodal, mostly a plateau with global minimum in a small central area.
It's defined only for 2 dimensions.
'''
class Easom(BenchmarkFunction):
	def __init__(self, opposite=False):
		super().__init__("Easom", 2, opposite)
	def _evaluate(self,point):
		ret = -math.cos(point[0])*math.cos(point[1])*math.exp(-pow(point[0]-math.pi,2)-pow(point[1]-math.pi,2))
		return ret

'''
Continuous, multimodal with an asymmetrical hight slope and global minimum on a plateau.
It's defined only for 2 dimensions.
'''
class GoldsteinAndPrice(BenchmarkFunction):
	def __init__(self, opposite=False):
		super().__init__("Goldstein and Price", 2, opposite)
	def _evaluate(self,point):
		a = 1.0 + pow(point[0]+point[1]+1.0,2)*(19.0-14.0*point[0]+3.0*pow(point[0],2)-14.0*point[1]+6.0*point[0]*point[1]+3.0*pow(point[1],2))
		b = 30.0 + pow(2*point[0]-3.0*point[1],2)*(18.0-32.0*point[0]+12.0*pow(point[0],2)+48.0*point[1]-36.0*point[0]*point[1]+27.0*pow(point[1],2))
		return a*b

'''
Continuous, non-convex and (highly) multimodal. 
Location of the minima are regularly distributed.
'''
class Rastrigin(BenchmarkFunction):
	def __init__(self, n_dimensions=2, opposite=False):
		super().__init__("Rastrigin", n_dimensions, opposite)
	def _evaluate(self,point):
		ret = sum([pow(p,2) - 10.0*math.cos(2.0*math.pi*p) for p in point]) + 10.0*len(point)
		return ret
	def _evaluate_derivative(self, point):
		return sum([2.0*p + 20.0*math.pi*math.sin(2.0*math.pi*p) for p in point])
	def _evaluate_second_derivative(self, point):
		return sum([2.0 + 40.0*pow(math.pi,2)*math.cos(2.0*math.pi*p) for p in point])

'''
Continuous, convex and unimodal.
'''
class Hypersphere(BenchmarkFunction):
	def __init__(self, n_dimensions=2, opposite=False):
		super().__init__("Hypersphere", n_dimensions, opposite)

	def _evaluate(self,point):
		ret = sum([pow(x,2) for x in point])
		return ret
	def _evaluate_derivative(self, point):
		return sum([2.0*x for x in point])
	def _evaluate_second_derivative(self, point):
		return 2.0*len(point)

class MartinGaddy(BenchmarkFunction):
	def __init__(self, opposite=False):
		super().__init__("Martin and Gaddy", 2, opposite)
	def _evaluate(self,point):
		ret = pow(point[0] - point[1],2) + pow((point[0] + point[1] - 10.0)/3.0,2) 
		return ret