import copy
import numpy as np
import numpy.random as rng

class Model:
	"""
	Abstract class that usable Models should inherit
	"""
	def __init__(self):
		"""
		Set the logLikelihood+tieBreaker tuple to nothing
		"""
		self.logL = [None, None]

	def fromPrior(self):
		"""
		Draw the parameters from the prior
		"""
		self.logL[1] = rng.rand()

	def calculateLogLikelihood(self):
		"""
		Define the likelihood function
		"""
		self.logL[0] = 0.0

	def perturb(self):
		"""
		Perturb, for metropolis
		"""
		self.logL[1] += 10.0**(1.5 - 6.0*rng.rand())*rng.randn()
		self.logL[1] = np.mod(self.logL[1], 1.0)

	def update(self, level):
		"""
		Do a Metropolis step wrt the given level
		"""
		assert self.logL >= level.logL
		proposal = copy.deepcopy(self)
		logH = proposal.perturb()
		if logH > 0.0:
			logH = 0.0
		if rng.rand() <= np.exp(logH) and proposal.logL >= level.logL:
			return [proposal, True]
		else:
			return [self, False]

if __name__ == '__main__':
	"""
	Simple main for testing
	"""
	m = Model()
	m.fromPrior()
	m2 = m.perturb()
	print(m is m2)


