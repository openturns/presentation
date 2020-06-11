'''
Perform sensitivity analysis on the Crue test-case. 

Reference
SaltelliSensitivityAlgorithm with LowDiscrepancyExperiment produces wrong results
https://github.com/openturns/openturns/issues/1005

The draw method of SobolSimulationAlgorithm can make OpenTURNS crash
https://github.com/openturns/openturns/issues/1001
'''

import openturns as ot
from openturns.viewer import View
from math import sqrt
import pylab as pl

#ot.RandomGenerator.SetSeed(0)

# 1. The function G
def functionCrue(X) :
    Q, Ks, Zv, Zm = X
    alpha = (Zm - Zv)/5.0e3
    H = (Q/(Ks*300.0*sqrt(alpha)))**(3.0/5.0)
    S = [H + Zv]
    return S

# Creation of the problem function
input_dimension = 4

g = ot.PythonFunction(input_dimension, 1, functionCrue) 
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

# 4. Create the joint distribution function, 
#    the output and the event. 
X = ot.ComposedDistribution([Q, Ks, Zv, Zm])
Y = ot.RandomVector(g, ot.RandomVector(X))

ot.Log.Show(ot.Log.DBG)

def progress(percent):
    print('-- progress=%.2f %%' % (percent))

alpha = 0.05
epsilon = 0.1
blocksize = 50
batchsize = 16

# By Chaos
S_exact = [0.489983, 0.166346, 0.320333, 0.00589773]
ST_exact = [0.507015,0.1824,0.321226,0.00685824]
for i in range(input_dimension):
    print("Exact X%d, S=%.4f \t ST=%.4f" % (i,S_exact[i],ST_exact[i]))

# Sensitivity analysis
estimator = ot.SaltelliSensitivityAlgorithm()
estimator.setUseAsymptoticDistribution(True)
algo = ot.SobolSimulationAlgorithm(X, g, estimator)
algo.setMaximumOuterSampling(100) # number of iterations
algo.setBlockSize(blocksize) # size of Sobol experiment at each iteration
algo.setBatchSize(batchsize) # number of points evaluated simultaneously
algo.setIndexQuantileLevel(alpha) # alpha
algo.setIndexQuantileEpsilon(epsilon) # epsilon
#algo.setProgressCallback(progress)
algo.run()
result = algo.getResult()
fo = result.getFirstOrderIndicesEstimate()
to = result.getTotalOrderIndicesEstimate()
print(fo)
print(to)

outerSampling = result.getOuterSampling()
print("OuterSampling = %d" % (outerSampling))

dist_fo = result.getFirstOrderIndicesDistribution()
dist_to = result.getTotalOrderIndicesDistribution()

pl.plot(range(input_dimension),fo,"ro",label="First Order")
pl.plot(range(input_dimension),to,"bx",label="Total Order")
pl.xlabel("Inputs")
pl.ylabel("Sensitivity indices")
size = g.getEvaluationCallsNumber()
pl.title("Sobol' indices - n=%d - 1-2 alpha=%.2f %%" % (size,(1-2*alpha)*100))
pl.axis([-0.5,input_dimension-0.5,-0.1,1.1])
print("Level alpha=%.4f" % (alpha))
for i in range(input_dimension):
    dist_fo_i = dist_fo.getMarginal(i)
    dist_to_i = dist_to.getMarginal(i)
    fo_ci = dist_fo_i.computeBilateralConfidenceInterval(1-2*alpha)
    to_ci = dist_to_i.computeBilateralConfidenceInterval(1-2*alpha)
    fo_ci_a = fo_ci.getLowerBound()[0]
    fo_ci_b = fo_ci.getUpperBound()[0]
    to_ci_a = to_ci.getLowerBound()[0]
    to_ci_b = to_ci.getUpperBound()[0]
    print("X%d, S in [%.4f,%.4f], ST in [%.4f,%.4f]" % (i,fo_ci_a,fo_ci_b,to_ci_a,to_ci_b))
    fo_cilength = fo_ci_b - fo_ci_a
    to_cilength = to_ci_b - to_ci_a
    print("    C.I.Length S - = %.4f, ST - = %.4f" % (fo_cilength, to_cilength))
    pl.plot([i,i],[fo_ci_a,fo_ci_b],"r-")
    pl.plot([i,i],[to_ci_a,to_ci_b],"b-")
pl.legend()
pl.savefig("crue-Sobol-indices.pdf")

for i in range(input_dimension):
    dist_fo_i = dist_fo.getMarginal(i)
    dist_to_i = dist_to.getMarginal(i)
    print("X%d, S=%s, ST=%s" % (i,str(dist_fo_i),str(dist_to_i)))

'''
Nombre d'évaluations

'''
nbiter = outerSampling * blocksize
print("Nb iterations = %d" % (nbiter))
nbfunceval = nbiter * (input_dimension + 2)
print("Nb function evaluations = %d" % (nbfunceval))

for i in range(input_dimension):
    dist_fo_i = dist_fo.getMarginal(i)
    graph = dist_fo_i.drawPDF()
    graph.setTitle("S%d" % (i))
    graph.setXTitle("S%d" % (i))
    graph.setLegends([""])
    View(graph)
    pl.savefig("S%d-distribution.pdf" % (i))
    dist_to_i = dist_to.getMarginal(i)
    graph = dist_to_i.drawPDF()
    graph.setTitle("ST%d" % (i))
    graph.setXTitle("ST%d" % (i))
    graph.setLegends([""])
    View(graph)
    pl.savefig("ST%d-distribution.pdf" % (i))

'''
View(algo.drawFirstOrderIndexConvergence())
View(algo.drawTotalOrderIndexConvergence())


'''

'''
saest = algo.getEstimator()
View(saest.DrawSobolIndices(["Q","Ks","Zv","Zm"],fo,to)) # OK

View(saest.draw()) # Fail
'''

'''
# Works 
size = 5000
inputDesign = ot.SobolIndicesExperiment(X, size).generate()
outputDesign = g(inputDesign)
sensitivityAnalysis = ot.SaltelliSensitivityAlgorithm(
    inputDesign, outputDesign, size)
View(sensitivityAnalysis.draw()) # OK
'''
