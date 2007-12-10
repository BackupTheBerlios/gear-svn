			

class VAR:
	def stampa (self):
		print 'VAR stampa'

	def specifico (self):
		print 'VAR specifico'

	def argomento (x):
		print 'VAR argomento: ' + str(x)		
		
		


class AppliedModel:
	def __init__(self,model):
		self.model = model

	def __getattr__ (self,name,*args):
		print args(0)
		f = getattr(self.model,name)
		if args[0] != None:
			print 'vero'
			return f(args)
		else:
			print 'falso'
			return f
	
	def specifico (self):
		print 'Specifico'
		return self.model.specifico()
		


 #==================================================================================================
 #============================================    MAIN     =========================================
 #==================================================================================================
if __name__ == "__main__":
	
	a = VAR()
	b = AppliedModel(a)

	b.stampa()
	#b.specifico()
	b.argomento(10)


