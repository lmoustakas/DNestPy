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
		for model in self.models:
			model.fromPrior()
			self.logLKeep.append(model.logl)
	#	while True:
	#		self.step()

	def step(self):
		which = rng.randint(options.numParticles)
		
		
#	def logPush(self):
		


if __name__ == '__main__':
	from TestModel import *
	s = Sampler(TestModel)
	s.run()
	print(s.logLKeep)
