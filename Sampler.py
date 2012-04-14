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
	Input: exampleModel
	"""
	def __init__(self, ModelType, options=Options()):
		self.options = options
		self.models = [ModelType()\
				for i in xrange(0, options.numParticles)]
		self.indices = [0 for i in xrange(0, options.numParticles)]
		self.levels = [Level()]
		self.logLKeep = []

	def run(self):
		for which in xrange(0, self.options.numParticles):
			self.models[which].fromPrior()
			self.updateLevelStatistics(which)

	#	while True:
	#		self.step()

	def step(self, numSteps=1):
		for i in xrange(0, numSteps):
			which = rng.randint(self.options.numParticles)
			[self.models[which], accepted] = self.models[which]\
				.update(self.levels[self.indices[which]])
			self.updateLevelStatistics(which, accepted)
		
	def updateLevelStatistics(self, which, accepted):
		if self.models[which].logL > self.levels[-1].logL\
			and len(self.levels) < self.options.maxNumLevels:
			self.logLKeep.append(self.models[which].logL)

		
#	def logPush(self):
		


if __name__ == '__main__':
	from TestModel import *
	s = Sampler(TestModel)
	s.run()
	s.step(20)
	print(s.logLKeep)

