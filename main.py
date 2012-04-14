from TestModel import *
from Sampler import *

options = Options()
options.load("OPTIONS")
sampler = Sampler(TestModel, options=options)
sampler.run()

