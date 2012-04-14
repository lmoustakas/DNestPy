from Model import *
import numpy as np
import numpy.random as rng

def logsumexp(logx1, logx2):
	"""
	Logarithmic addition
	"""
	biggest = np.max([logx1, logx2])
	logx1_ = logx1 - biggest
	logx2_ = logx2 - biggest
	result = np.log(np.sum(np.exp([logx1_, logx2_])))
	result += biggest
	return result


class TestModel(Model):
	"""
	An example model
	"""
	def __init__(self):
		Model.__init__(self)
		self.params = np.zeros(20)

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
		u = 0.01
		v = 0.1
		C = np.log(1.0/np.sqrt(2.0*np.pi))
		logL1 = -len(self.params)*(C + np.log(u)) - 0.5*np.sum((self.params/u)**2)
		logL2 = -len(self.params)*(C + np.log(v)) - 0.5*np.sum((self.params/v)**2)
		self.logL[0] = logsumexp(logL1, logL2)

	def __str__(self):
		return "".join(str(i) + " " for i in self.params)

if __name__ == '__main__':
	from Level import *
	l = Level()
	t = TestModel()
	t.fromPrior()
	for i in xrange(0, 1000):
		t = t.update(l)[0]
		print(str(t))

