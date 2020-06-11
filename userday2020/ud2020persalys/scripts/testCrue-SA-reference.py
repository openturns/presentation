from openturns.viewer import View
import openturns as ot
from math import sqrt
import pylab as pl

ot.RandomGenerator.SetSeed(0)

# 1. The function G
def functionCrue(X) :
    Q, Ks, Zv, Zm = X
    alpha = (Zm - Zv)/5.0e3
    H = (Q/(Ks*300.0*sqrt(alpha)))**(3.0/5.0)
    S = [H + Zv]
    return S

# Creation of the problem function
g = ot.PythonFunction(4, 1, functionCrue) 

# 2. Random vector definition
myParamQ = ot.GumbelAB(1013., 558.)
Q = ot.ParametrizedDistribution(myParamQ)
otLOW = ot.TruncatedDistribution.LOWER
Q = ot.TruncatedDistribution(Q, 0, otLOW)
Ks = ot.Normal(30.0, 7.5)
Ks = ot.TruncatedDistribution(Ks, 0, otLOW)
Zv = ot.Uniform(49.0, 51.0)
Zm = ot.Uniform(54.0, 56.0)

# 4. Create the joint distribution function, 
#    the output and the event. 
X = ot.ComposedDistribution([Q, Ks, Zv, Zm])
Y = ot.RandomVector(g, ot.RandomVector(X))


# Works 
size = 100000
inputDesign = ot.SobolIndicesExperiment(X, size).generate()
outputDesign = g(inputDesign)
sensitivityAnalysis = ot.SaltelliSensitivityAlgorithm(
    inputDesign, outputDesign, size)
View(sensitivityAnalysis.draw()) # OK

dist_fo = sensitivityAnalysis.getFirstOrderIndicesDistribution()
dist_to = sensitivityAnalysis.getTotalOrderIndicesDistribution()

alpha = 0.1
input_dimension = X.getDimension()
for i in range(input_dimension):
    dist_fo_i = dist_fo.getMarginal(i)
    dist_to_i = dist_to.getMarginal(i)
    fo_ci = dist_fo_i.computeBilateralConfidenceInterval(1-alpha)
    to_ci = dist_to_i.computeBilateralConfidenceInterval(1-alpha)
    fo_ci_a = fo_ci.getLowerBound()[0]
    fo_ci_b = fo_ci.getUpperBound()[0]
    to_ci_a = to_ci.getLowerBound()[0]
    to_ci_b = to_ci.getUpperBound()[0]
    print("S[%d] in [%.4f,%.4f] at %4f" % (i,fo_ci_a,fo_ci_b,1-alpha))
    print("ST[%d] in [%.4f,%.4f] at %4f" % (i,to_ci_a,to_ci_b,1-alpha))
