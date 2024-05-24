# -*- coding: utf-8 -*-
# Copyright (C) - 2013 - 2018 - Michael Baudin - EDF R&D

# For OT v1.11

import openturns as ot
import math
import openturns.coupling_tools as ct


def mySimulator(X):
    # 1. Create input file
    infile = "input_template.txt"
    outfile = "input.py"
    tokens = ["@X0", "@X1", "@X2"]
    ct.replace(infile, outfile, tokens, X)
    # 2. Compute
    program = "python external_program.py"
    cmd = program + " " + outfile
    ct.execute(cmd)
    # 3. Parse output file
    Y = ct.get("output.txt", tokens=["Y0=", "Y1="])
    return Y


myWrapper = ot.PythonFunction(3, 2, mySimulator)

# Create the marginal distributions
distributionX0 = ot.Normal(0.0, 1.0)
distributionX1 = ot.Normal(0.0, 1.0)
distributionX2 = ot.Normal(0.0, 1.0)

# Create the input probability distribution
inputDistribution = ot.ComposedDistribution(
    (distributionX0, distributionX1, distributionX2)
)

# Create the input random vector
inputRandomVector = ot.RandomVector(inputDistribution)

# Create the output variable of interest
outputVariableOfInterest = ot.RandomVector(myWrapper, inputRandomVector)

# Probabilistic Study: central dispersion
montecarlosize = 10

# Start the simulations
outputSample = outputVariableOfInterest.getSample(montecarlosize)

# Get the empirical mean and standard deviations
outputDim = myWrapper.getOutputDimension()
empiricalMean = outputSample.computeMean()
empiricalSd = outputSample.computeStandardDeviationPerComponent()
for i in range(outputDim):
    print(
        "Mean(Y(%d))=%f, Sd.Dev.(Y(%d))=%f" % (i, empiricalMean[i], i, empiricalSd[i])
    )

print("Exact Mean(Y(0))=", 0, " St.Dev.(Y(0))=", math.sqrt(3))
print("Exact Mean(Y(1))=", 0, " St.Dev.(Y(1))~", 1.415)
