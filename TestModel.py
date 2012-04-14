from Model import *
import numpy as np
import numpy.random as rng

def logsumexp(values):
	"""
	Logarithmic addition
	"""
	biggest = np.max(values)
	x = values - biggest
	result = np.log(np.sum(np.exp(x))) + biggest
	return result


class TestModel(Model):
	"""
	An example model
	"""
	u = 0.01
	v = 0.1
	logu = np.log(u)
	logv = np.log(v)
	C = np.log(1.0/np.sqrt(2.0*np.pi))
	w = np.log(100.0)

	def __init__(self):
		Model.__init__(self)
		self.numParams = 20
		self.params = np.zeros(self.numParams)

	def fromPrior(self):
		"""
		Generate all parameters iid from U(-0.5, 0.5)
		"""
		self.params = -0.5 + rng.rand(self.params.size)		
		Model.fromPrior(self)
		self.calculateLogLikelihood()

	def perturb(self):
		"""
		Metropolis proposal: perturb one parameter
		"""
		logH = 0.0
		which = rng.randint(self.params.size)
		self.params[which] += 10.0**(1.5 - 6.0*rng.rand())*rng.randn()
		self.params[which] = np.mod(self.params[which] + 0.5,\
					1.0) - 0.5
		Model.perturb(self)
		self.calculateLogLikelihood()
		return logH

	def calculateLogLikelihood(self):
		"""
		Likelihood function: Mixture of two Gaussians
		"""
		logL1 = self.numParams*TestModel.C
		logL1 += -self.numParams*TestModel.logu - 0.5*np.sum(((self.params - 0.031)/TestModel.u)**2)
		logL2 = self.numParams*TestModel.C
		logL2 += -self.numParams*TestModel.logv - 0.5*np.sum((self.params/TestModel.v)**2)
		self.logL[0] = logsumexp([TestModel.w + logL1, logL2])

	def __str__(self):
		return "".join(str(i) + " " for i in self.params)

