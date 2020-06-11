from openturns.viewer import View
import openturns as ot
from math import sqrt
import pylab as pl

ot.RandomGenerator.SetSeed(0)

# 1. The function G
def functionCrue(X) :
    Q, Ks, Zv, Zm = X
    L = 5.0e3
    B = 300.0
    alpha = (Zm - Zv)/L
    H = (Q/(Ks*B*sqrt(alpha)))**(3.0/5.0)
    S = [H + Zv]
    return S

# Creation of the problem function
g = ot.PythonFunction(4, 1, functionCrue) 
g = ot.MemoizeFunction(g)

# 2. Random vector definition
myParamQ = ot.GumbelAB(1013., 558.)
Q = ot.ParametrizedDistribution(myParamQ)
otLOW = ot.TruncatedDistribution.LOWER
Q = ot.TruncatedDistribution(Q, 0, otLOW)
Ks = ot.Normal(30.0, 7.5)
Ks = ot.TruncatedDistribution(Ks, 0, otLOW)
Zv = ot.Uniform(49.0, 51.0)
Zm = ot.Uniform(54.0, 56.0)

# 3. View the PDF
Q.setDescription(["Q (m3/s)"])
Ks.setDescription(["Ks (m^(1/3)/s)"])
Zv.setDescription(["Zv (m)"])
Zm.setDescription(["Zm (m)"])

View(Q.drawPDF()).show()
pl.savefig("Q.pdf")

View(Ks.drawPDF()).show()
View(Zv.drawPDF()).show()
View(Zm.drawPDF()).show()

# 4. Create the joint distribution function, 
#    the output and the event. 
X = ot.ComposedDistribution([Q, Ks, Zv, Zm])
Y = ot.RandomVector(g, ot.RandomVector(X))


# 6. Estimate expectation with algorithm
algo = ot.ExpectationSimulationAlgorithm(Y)
algo.setMaximumOuterSampling(1000)
algo.setBlockSize(10)
algo.setMaximumCoefficientOfVariation(0.001)
algo.run()
result = algo.getResult()
expectation = result.getExpectationEstimate()
print("Mean by ESA = %f " % expectation[0])
expectationDistribution = result.getExpectationDistribution()
graph = expectationDistribution.drawPDF()
graph.setTitle("")
graph.setXTitle("Mean river height estimate")
graph.setLegends([""])
View(graph)
pl.savefig("MeanDistribution.pdf")

# Check accuracy
n = g.getCallsNumber()
print("Number of calls to G = %d" % n)
cv = result.getCoefficientOfVariation()[0]
print("Coef. of var.=%.6f" % (cv))
outputSample = g.getOutputHistory()
e = outputSample.computeMean()[0]
s = outputSample.computeStandardDeviationPerComponent()[0]
trueCV = s/e/sqrt(n)
print("True CV=%f" % (trueCV))

'''
# 5. Estimate expectation with simple Monte-Carlo
sampleSize = 10000
sampleX = X.getSample(sampleSize)
sampleY = g(sampleX)
sampleMean = sampleY.computeMean()
print("Mean by MC = %f" % (sampleMean[0]))
'''

'''
# Sensitivity analysis
estimator = ot.SaltelliSensitivityAlgorithm()
estimator.setUseAsymptoticDistribution(True)
algo = ot.SobolSimulationAlgorithm(X, g, estimator)
algo.setMaximumOuterSampling(25) # number of iterations
algo.setBlockSize(100) # size of Sobol experiment at each iteration
algo.setBatchSize(4) # number of points evaluated simultaneously
algo.setIndexQuantileLevel(0.05) # alpha
algo.setIndexQuantileEpsilon(1e-2) # epsilon
algo.run()
result = algo.getResult()
fo = result.getFirstOrderIndicesEstimate()
print("First order:")
print(fo)
to = result.getTotalOrderIndicesEstimate()
print("Total order:")
print(to)
foDist = result.getFirstOrderIndicesDistribution()
saest = algo.getEstimator()

# View(saest.draw()) Fail

View(saest.DrawSobolIndices(["Q","Ks","Zv","Zm"],fo,to))
'''