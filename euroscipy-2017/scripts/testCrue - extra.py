from openturns.viewer import View
from numpy import inf
from openturns import (
    ComposedDistribution, Gumbel, 
    RandomVector, Normal, PythonFunction, MonteCarlo, 
    TruncatedDistribution, Event, Uniform, GreaterOrEqual
)
from math import sqrt

def functionCrue(X) :
    H_d = 3.0
    Z_b = 55.5
    L = 5.0E3
    B = 300.0
    Z_d = Z_b + H_d
    Q, K_s, Z_v, Z_m = X
    alpha = (Z_m - Z_v)/L
    H = (Q/(K_s*B*sqrt(alpha)))**(3.0/5.0)
    Z_c = H + Z_v
    return [Z_c - Z_d]

# Creation of the problem function
inputDim = 4 # Input dimension
f = PythonFunction(inputDim, 1, functionCrue) 
f.enableHistory()

# Random vector definition
Qmu=1013.
Qsigma=558.
Q = Gumbel(1./Qsigma, Qmu)
Q = TruncatedDistribution(Q, 0, inf)
K_s = Normal(30.0, 7.5)
K_s = TruncatedDistribution(K_s, 0, inf)
Z_v = Uniform(49.0, 51.0)
Z_m = Uniform(54.0, 56.0)

Q.setDescription(["Q (m3/s)"])
K_s.setDescription(["Ks (m^(1/3)/s)"])
Z_v.setDescription(["Zv (m)"])
Z_m.setDescription(["Zm (m)"])

View(Q.drawPDF()).show()
View(K_s.drawPDF()).show()
View(Z_v.drawPDF()).show()
View(Z_m.drawPDF()).show()

inputRandomVector = ComposedDistribution([Q, K_s, Z_v, Z_m])
outputRandomVector = RandomVector(f, RandomVector(inputRandomVector))
eventF = Event(outputRandomVector, GreaterOrEqual(), 0) 

algoProb = MonteCarlo(eventF)
algoProb.setMaximumCoefficientOfVariation(0.05)
algoProb.setMaximumOuterSampling(100000)
algoProb.run()

# Results
resultAlgo = algoProb.getResult()
Neval = f.getEvaluationCallsNumber()
Pf = resultAlgo.getProbabilityEstimate()
print "Failure Probability =%e" % (Pf)
c95 = resultAlgo.getConfidenceLength()
pmin=Pf-0.5*c95
pmax=Pf+0.5*c95
print "within [%e,%e]" % (pmin,pmax)
cov=resultAlgo.getCoefficientOfVariation()
print "C.O.V: %.1f%%" % (cov*100)

from openturns import VisualTest
outComputedPoints = f.getOutputHistory().getSample()
histoGraph = VisualTest.DrawHistogram(outComputedPoints,300)
histoGraph.setTitle("Histogramme de la surverse")
histoGraph.setXTitle("S (m)")
histoGraph.setYTitle("Frequence")
histoGraph.setBoundingBox([-10,5,0,0.40])
histoGraph.setLegends([""])
View(histoGraph).show()
