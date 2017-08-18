from openturns.viewer import View
from numpy import inf
from openturns import (
    ComposedDistribution, Gumbel, 
    RandomVector, Normal, PythonFunction, MonteCarlo, 
    TruncatedDistribution, Event, Uniform, GreaterOrEqual, 
    Pairs
)
from math import sqrt

# 1. The function G
def functionCrue(X) :
    Q, Ks, Zv, Zm = X
    alpha = (Zm - Zv)/5.0e3
    H = (Q/(Ks*300.0*sqrt(alpha)))**(3.0/5.0)
    S = [H + Zv - (55.5 + 3.0)]
    return S

# Creation of the problem function
f = PythonFunction(4, 1, functionCrue) 
f.enableHistory()

# 2. Random vector definition
Q = Gumbel(1./558., 1013.)
Q = TruncatedDistribution(Q, 0, inf)
Ks = Normal(30.0, 7.5)
Ks = TruncatedDistribution(Ks, 0, inf)
Zv = Uniform(49.0, 51.0)
Zm = Uniform(54.0, 56.0)

# 3. View the PDF
Q.setDescription(["Q (m3/s)"])
Ks.setDescription(["Ks (m^(1/3)/s)"])
Zv.setDescription(["Zv (m)"])
Zm.setDescription(["Zm (m)"])

View(Q.drawPDF()).show()
View(Ks.drawPDF()).show()
View(Zv.drawPDF()).show()
View(Zm.drawPDF()).show()

# 4. Create the joint distribution function, 
#    the output and the event. 
inputvector = ComposedDistribution([Q, Ks, Zv, Zm])
outputvector = RandomVector(f, RandomVector(inputvector))
eventF = Event(outputvector, GreaterOrEqual(), 0) 

# 4.bis Draw pairs
sample = inputvector.getSample(500)
myPairs = Pairs(sample, "N=500", sample.getDescription(), "red", "bullet")
View(myPairs).show()

# 5. Create the Monte-Carlo algorithm
algoProb = MonteCarlo(eventF)
algoProb.setMaximumOuterSampling(100000)
algoProb.run()

# 6. Get the results
resultAlgo = algoProb.getResult()
neval = f.getEvaluationCallsNumber()
print "Number of function calls =", neval
pf = resultAlgo.getProbabilityEstimate()
print "Failure Probability = %e" % (pf)
c95 = resultAlgo.getConfidenceLength()
pmin=pf-0.5*c95
pmax=pf+0.5*c95
print "within [%e,%e]" % (pmin,pmax)

# 7. Plot the histogram
from openturns import VisualTest
outComputedPoints = f.getOutputHistory().getSample()
histoGraph = VisualTest.DrawHistogram(outComputedPoints,100)
histoGraph.setTitle("Histogramme de la surverse")
histoGraph.setXTitle("S (m)")
histoGraph.setYTitle("Frequence")
histoGraph.setBoundingBox([-10,5,0,0.40])
histoGraph.setLegends([""])
View(histoGraph).show()

