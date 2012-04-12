import copy
import numpy as np
import numpy.random as rng

class Model:
	"""
	Abstract class that usable Models should inherit
	"""
	def __init__(self):
		"""
		Set the loglikelihood+tieBreaker tuple to nothing
		"""
		self.logl = [None, None]

	def fromPrior(self):
		"""
		Draw the parameters from the prior
		"""
		self.logl[1] = rng.rand()
		self.calculateLogLikelihood()

	def calculateLogLikelihood(self):
		"""
		Define the likelihood function
		"""
		self.logl[0] = 0.0

	def perturb(self):
		"""
		Perturb, for metropolis
		"""
		self.logl[1] += 10.0**(1.5 - 6.0*rng.rand())*rng.randn()
		self.logl[1] = np.mod(self.logl[1], 1.0)
		return 0.0

	def update(self, level):
		"""
		Do a Metropolis step wrt the given level
		"""
		assert self.logl >= level
		proposal = copy.deepcopy(self)
		logH = proposal.perturb()
		if logH > 0.0:
			logH = 0.0
		if rng.rand() <= exp(logH) and proposal.logl >= level:
			return proposal
		else:
			return self

if __name__ == '__main__':
	"""
	Simple main for testing
	"""
	m = Model()
	m.fromPrior()
	m2 = m.perturb()
	print(m is m2)


