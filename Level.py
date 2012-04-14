import numpy as np

class Level:
	"""
	Defines a Nested Sampling level
	"""
	def __init__(self, logX=0.0, logL=[-1E300, 0.0]):
		"""
		Construct a level. By default, logX = 0
		and logL = [-1E300, 0.0]. i.e. the prior.
		I use -1E300 for compatibility with the C++ version.
		"""
		self.logX, self.logL = logX, logL
		self.accepts = 0
		self.tries = 0
		self.exceeds = 0
		self.visits = 0

	def __str__(self):
		s = str(self.logX) + " " + str(self.logL[0]) + " " \
			+ str(self.logL[1]) + " "\
			+ str(self.accepts) + " "\
			+ str(self.tries) + " " + str(self.exceeds) + " "\
			+ str(self.visits) + " "
		return s

class LevelSet:
	"""
	Defines a set of levels. Implemented as a list
	"""
	def __init__(self, filename=None):
		"""
		Optional: load from file `filename`
		"""
		self.levels = []

		if filename != None:
			f = open('levels.txt', 'r')
			lines = f.readlines()
			for l in lines:
				stuff = l.split()
				level = Level(logX=float(stuff[0])\
				,logL=[float(stuff[1]), float(stuff[2])])
				level.accepts = int(stuff[3])
				level.tries = int(stuff[4])
				level.exceeds = int(stuff[5])
				level.visits = int(stuff[6])
				self.levels.append(level)

	def __str__(self):
		return "".join([str(l) + '\n' for l in self.levels])

if __name__ == '__main__':
	levels = LevelSet('levels.txt')
	print(levels)

