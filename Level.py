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
		"""
		Represent the level as a string
		"""
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
		self.logLKeep = [] # Accumulation, for making new levels

		if filename == None:
			# Start with one level, the prior
			self.levels.append(Level())
		else:
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
			f.close()

	def updateAccepts(self, index, accepted):
		"""
		Input: `index`: which level particle was in
		`accepted`: whether it was accepted or not
		"""
		self.levels[index].accepts += int(accepted)
		self.levels[index].tries += 1

	def updateExceeds(self, index, exceeds):
		"""
		Input: `index`: which level particle is in
		`exceeds`: whether it exceeds the level above
		"""
		print("Level.updateExceeds not implemented yet")
		pass

	def updateLogLKeep(self, logL):
		"""
		If the logLikelihood is above the highest level,
		store it.
		Input: logLikelihood seen
		"""
		if logL > self.levels[-1].logL:
			self.logLKeep.append(logL)

	def maybeAddLevel(self, newLevelInterval):
		added = False
		if len(self.logLKeep) >= newLevelInterval:
			self.logLKeep = sorted(self.logLKeep)
			index = int(0.63212*len(self.logLKeep))
			print("# Creating level " + str(len(self.levels))\
				+ " with logL = "\
				+ str(self.logLKeep[index][0]))
			newLevel = Level(self.levels[-1].logX - 1.0,\
					self.logLKeep[index])
			self.levels.append(newLevel)
			self.logLKeep = self.logLKeep[index+1:]
			added = True
		return added

	def save(self, filename='levels.txt'):
		"""
		Write out all of the levels to a text file.
		Default filename='levels.txt'
		"""
		f = open(filename, 'w')
		f.write(str(self))
		f.close()

	def __getitem__(self, i):
		"""
		This is like overloading operator [] (LevelSet, int)
		"""
		return self.levels[i]

	def __str__(self):
		"""
		Put all levels in a single string, each level on a line
		"""
		return "".join([str(l) + '\n' for l in self.levels])

	def __len__(self):
		"""
		Return number of levels
		"""
		return len(self.levels)

if __name__ == '__main__':
	levels = LevelSet()
	levels.save('test.txt')

