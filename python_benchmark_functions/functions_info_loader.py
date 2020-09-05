"""
This document for benchmark functions is provided by supervisor
"""

import os, json

path_info = os.path.join(os.path.dirname(os.path.abspath(__file__)),"functions_info.json")

class Reference(object):
	def __init__(self, raw_data):
		data=raw_data.strip()
		if data[0]!="@" or data[-1]!="}":
			raise ValueError("Problems in formatting the following reference: "+raw_data)
		self.paper_type, json_raw = data[1:].split("{")
		self.data = json.load("{"+json_raw)
	def __str_(self):
		return '@'+self.paper_type+str(self.data)

class FunctionsInfo(object):
	def __init__(self):
		self.load()

	def load(self):
		f=open(path_info)
		self.config = json.load(f)
		f.close()

	def save(self):
		f=open(path_info,'w')
		f.write(json.dumps(self.config,indent=2))
		f.close()

	def _parameters2str(self,parameters):
		return ','.join([p+'='+str(v) for p,v in parameters])

	def add_function(self, function_name, parameters=[]):
		if function_name not in self.config:
			if len(parameters)==0:
				self.config[function_name]={'minima':{},'suggested bounds':{}}
			else:
				pn=self._parameters2str(parameters)
				self.config[function_name]={pn:{'minima':{},'suggested bounds':{}}}

	def add_optimum(self, function_name, value, position, parameters=[], isMaximum=False, dimensions_invariant=False):
		name=function_name.upper()
		self.add_function(name, parameters)
		if isMaximum:
			optimum_type="maxima"
		else:
			optimum_type="minima"
		if len(parameters)==0:
			vals=self.config[name][optimum_type]
		else:
			pn=self._parameters2str(parameters)
			if pn not in self.config[name]:
				self.config[name][pn]={'minima':{},'suggested bounds':{} }
			vals=self.config[name][pn][optimum_type]
		if dimensions_invariant:
			dim='*'
		else:
			dim=str(len(position))
		if dim not in vals:
			vals[dim]=[]
		vals[dim]+=[position]

	# auxiliary function
	def _get_solutions(self,function_name,n_dimensions,optimum_type,parameters=[]):
		name=function_name.upper()
		ret=[]
		if optimum_type not in self.config[name]:
			return []
		if len(parameters)==0:
			vals=self.config[name][optimum_type]
		else:
			pn=self._parameters2str(parameters)
			if pn not in self.config[name]:
				return []
			vals=self.config[name][pn][optimum_type]
		if '*' in vals:
			ret+=[[vals['*'][0][0]]*n_dimensions] # this is just a workaround to make the call consistent
		if str(n_dimensions) in vals:
			ret+=vals[str(n_dimensions)]
		return ret

	# returns all the known minima
	def get_minima(self,function_name,n_dimensions,parameters=[]):
		return self._get_solutions(function_name,n_dimensions,"minima",parameters)

	# returns all the known maxima
	def get_maxima(self,function_name,n_dimensions,parameters=[]):
		return self._get_solutions(function_name,n_dimensions,"maxima",parameters)
	
	def suggested_bounds(self, function_name, lower_bound, upper_bound, parameters=[]):
		name=function_name.upper()
		self.add_function(name, parameters)
		if len(parameters)==0:
			vals=self.config[name]["suggested bounds"]
		else:
			pn=self._parameters2str(parameters)
			if pn not in self.config[name]:
				self.config[name][pn]={'minima':{},'suggested bounds':{} }
			vals=self.config[name][pn]["suggested bounds"]
		vals["lower"] = lower_bound
		vals["upper"] = upper_bound
	
	def get_suggested_bounds(self, function_name, parameters=[]):
		name=function_name.upper()
		if len(parameters)==0:
			vals=self.config[name]["suggested bounds"]
		else:
			pn=self._parameters2str(parameters)
			vals=self.config[name][pn]["suggested bounds"]
		return (vals["lower"], vals["upper"])

	def get_reference(self, function_name):
		name=function_name.upper()
		if name not in self.config or "reference" not in self.config[name]:
			return None
		return Reference(self.config[name]["reference"])