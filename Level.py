import numpy as np

class Level:
	"""
	Defines a Nested Sampling level
	"""
	def __init__(self, logX=0.0, logL=[-np.inf, 0.0]):
		"""
		Construct a level
		"""
		self.logX, self.logL = logX, logL
		self.tries = 0
		self.accepts = 0
		self.visits = 0
		self.exceeds = 0

if __name__ == '__main__':
	level = Level()
	print(level)

