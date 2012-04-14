from Model import *
from Level import *

class Options:
	"""
	DNest Options
	"""
	def __init__(self, numParticles=1, newLevelInterval=10000,\
			saveInterval=10000, lamb=10.0, beta=10.0,
			maxNumLevels=100):
		self.numParticles = numParticles
		self.newLevelInterval = newLevelInterval
		self.saveInterval = saveInterval
		self.lamb = lamb
		self.beta = beta
		self.maxNumLevels = maxNumLevels

class Sampler:
	"""
	A single DNest sampler.
	"""
	def __init__(self, ModelType, options=Options(), levelsFile=None):
		"""
		Input: The class to be used
		Optional: `options`: Options object
		`levelsFile`: Filename to load pre-made levels from
		"""
		self.options = options
		self.models = [ModelType()\
				for i in xrange(0, options.numParticles)]
		self.indices = [0 for i in xrange(0, options.numParticles)]
		self.levels = LevelSet(levelsFile)

	def run(self):
		"""
		Initialise the models from the prior, and then run the sampler!
		"""
		for which in xrange(0, self.options.numParticles):
			self.models[which].fromPrior()
			self.updateVisits(which)

	#	while True:
	#		self.step()

	def step(self, numSteps=1):
		"""
		Take numSteps steps of the sampler. default=1
		"""
		for i in xrange(0, numSteps):
			which = rng.randint(self.options.numParticles)
			[self.models[which], accepted] = self.models[which]\
				.update(self.levels[self.indices[which]])
			self.updateVisits(which)
		
	def updateVisits(self, which):
		"""
		Update visits/exceeds level statistics
		and logLKeep
		"""
		if self.models[which].logL > self.levels[-1].logL\
			and len(self.levels) < self.options.maxNumLevels:
			self.logLKeep.append(self.models[which].logL)

		index = self.indices[which]
		if index < len(self.levels) - 1:
			self.levels[index].visits += 1
			if self.models[which].logL > self.levels[index+1].logL:
				self.levels[index].exceeds += 1
		
#	def logPush(self):
		


if __name__ == '__main__':
	from TestModel import *
	s = Sampler(TestModel)
	s.run()
	s.step(20)
	print(s.logLKeep)
	print s.levels[0]

