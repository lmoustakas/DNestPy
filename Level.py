import numpy as np

class Level:
	"""
	Defines a Nested Sampling level
	"""
	def __init__(self, logX=0.0, logL=[-np.inf, 0.0]):
		"""
		Construct a level. By default, logX = 0
		and logL = [-np.inf, 0.0]. i.e. the prior.
		"""
		self.logX, self.logL = logX, logL
		self.tries = 0
		self.accepts = 0
		self.visits = 0
		self.exceeds = 0

	def __str__(self):
		s = str(self.logX) + " " + str(self.logL[0]) + " " \
			+ str(self.logL[1]) + " "\
			+ str(self.tries) + " "\
			+ str(self.accepts) + " " + str(self.visits) + " "\
			+ str(self.exceeds) + " "
		return s

if __name__ == '__main__':
	level = Level()
	print(level)

