from openturns import *
from IntegralUserDefined import *
from IntegralUserDefinedFactory import *

support = [1, 2, 3, 4]
weights = [0.1, 0.2, 0.3, 0.8]

d = IntegralUserDefined(support, weights)
print "d=", d
sample = d.getNumericalSample(10000)
d2 = IntegralUserDefinedFactory().buildImplementation(sample)
print "d2=", d2
