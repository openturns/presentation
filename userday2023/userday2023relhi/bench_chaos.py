#! /usr/bin/env python

import openturns as ot
import openturns.experimental as otexp
from openturns.usecases import ishigami_function as ishigami_function
import time

ot.TESTPREAMBLE()
#ot.Log.Show(ot.Log.INFO)
# Extract the relevant elements of the Ishigami test-case
im = ishigami_function.IshigamiModel()
dimension = im.dim
model = im.model

marginals = [im.X1, im.X2, im.X3]
distribution = im.distributionX

# Create the orthogonal basis
polynomialCollection = [ot.LegendreFactory()] * dimension

enumerateFunction = ot.LinearEnumerateFunction(dimension)
productBasis = ot.OrthogonalProductPolynomialFactory(polynomialCollection, enumerateFunction)

# Create the doe
degree = 12
basisSize = enumerateFunction.getBasisSizeFromTotalDegree(degree)
samplingSize = 8192
print("basisSize=", basisSize)
doe = ot.LowDiscrepancyExperiment(ot.LowDiscrepancySequence(ot.SobolSequence()), distribution, samplingSize)


# Sampling
inputSample, weights = doe.generateWithWeights()
outputSample = model(inputSample)


for integration in [True, False]:
    if integration:
        algo = otexp.IntegrationExpansion(inputSample, weights, outputSample, distribution, productBasis, basisSize)
        tic = time.time()
        algo.run()
        toc = time.time()
        print(algo.getClassName() + " Elapsed time : ", toc - tic, integration)
    else:
        for methodName in ["SVD", "QR", "Cholesky"]:
            algo = otexp.LeastSquaresExpansion(inputSample, weights, outputSample, distribution, productBasis, basisSize, methodName)
            tic = time.time()
            algo.run()
            toc = time.time()
            print(algo.getClassName() + "/"+methodName + " time=", toc - tic)

    if integration:
        projectionStrategy = ot.IntegrationStrategy()
    else:
        projectionStrategy = ot.LeastSquaresStrategy()
    adaptiveStrategy = ot.FixedStrategy(productBasis, basisSize)
    algo = ot.FunctionalChaosAlgorithm(inputSample, weights, outputSample, distribution, adaptiveStrategy, projectionStrategy)
    tic = time.time()
    algo.run()
    toc = time.time()
    print("FunctionalChaosAlgorithm/"+ projectionStrategy.getClassName()+ " time=", toc - tic)
