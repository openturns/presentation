# -*- coding: utf-8 -*-
"""
Objectif : paramétrer la précision d'estimation de la moyenne 
en fonction d'un coefficient de variation.

Reference
http://www.epixanalytics.com/modelassist/CrystalBall/Model_Assist.htm#Montecarlo/Precision_control_feature.htm
"""
import numpy as np
import openturns as ot
from centraldispersion import (
centralDispersionByMonteCarlo, 
centralDispersionPrintResults, 
centralDispersionPrintParameters
)

# 1. The function G
def functionCrue(X) :
    Q, Ks, Zv, Zm = X
    L = 5.0e3
    B = 300.0
    alpha = (Zm - Zv)/L
    H = (Q/(Ks*B*np.sqrt(alpha)))**(3.0/5.0)
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

# 4. Create the joint distribution function, 
#    the output and the event. 
X = ot.ComposedDistribution([Q, Ks, Zv, Zm])
Y = ot.RandomVector(g, ot.RandomVector(X))

# User parameters
blocksize=1000
maxiter=100
maxcov=0.001 # Criteria B
maxcalls=maxiter * blocksize # Criteria A
maxelapsetime=5 # Criteria C
alpha=0.05 # Niveau de confiance de l'intervalle

# 6. Estimate expectation with algorithm
print("\ncentralDispersionByMonteCarlo")
centralDispersionPrintParameters(blocksize, maxcov, maxcalls,maxelapsetime,alpha)

outputSample, criteria=centralDispersionByMonteCarlo(Y, blocksize,maxcov,maxcalls,maxelapsetime)
if (criteria==1):
    print("Reached number of calls")
elif (criteria==2):
    print("Reached required precision")
elif (criteria==3):
    print("Reached maximum elapsed time")
    
centralDispersionPrintResults(outputSample,alpha)

# 7. Estimate expectation with ExpectationSimulationAlgorithm
print("\nExpectationSimulationAlgorithm")
g.clearHistory()
ot.Log.Show(ot.Log.DBG)
algo = ot.ExpectationSimulationAlgorithm(Y)
algo.setMaximumOuterSampling(maxiter)
algo.setBlockSize(blocksize)
algo.setMaximumCoefficientOfVariation(maxcov)
algo.run()
result = algo.getResult()
expectation = result.getExpectationEstimate()
print("Mean by ESA = %f " % expectation[0])
print("CV(Mean) = %.2f %% " % (100*result.getCoefficientOfVariation()[0]))
print("Number of function calls = %d" % (g.getInputHistory().getSize()))

