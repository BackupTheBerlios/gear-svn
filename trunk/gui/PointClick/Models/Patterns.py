

class Dataset:
	def __init__(self,x):
		self.data = x

class Model():
	def run (self,stp):
			

class VAR(Model):
	def __init__(self):



class AppliedModel():
	def __init__(self,data,model):
		self.data = data
		self.model = model
		self.estimated = False 


	def __getattr__ (self,name):
		return getattr(self.model,name)
	
	def run (self):
		return self.model.run(self.data)
	

		

	def ChangeData (self,data):
		self.data = data
	
	def ChangeModel (self,model):
		self.model = model
	

		
		
		



