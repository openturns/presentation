"""
Kriging: metamodel with continuous and categorical variables
============================================================
"""
# %%
# We consider here the surrogate modeling of an analytical function characterized by
# continuous and categorical variables
#

# %%
import openturns as ot
import openturns.experimental as otexp
import numpy as np
import matplotlib.pyplot as plt

# Seed chosen in order to obtain a visually nice plot
ot.RandomGenerator.SetSeed(5)

# %%
# We first show the advantage of modeling the various levels of a mixed
# continuous / categorical function through a single surrogate model
# on a simple test-case taken from [pelamatti2020]_, defined below.


# %%
def illustrativeFunc(inp):
    x, z = inp
    y = np.cos(7 * x) + 0.5 * z
    return [y]


dim = 2
fun = ot.PythonFunction(dim, 1, illustrativeFunc)
numberOfZLevels = 2  # Number of categorical levels for z
# Input distribution
dist = ot.ComposedDistribution(
    [ot.Uniform(0, 1), ot.UserDefined(ot.Sample.BuildFromPoint(range(numberOfZLevels)))]
)

# %%
# In this example, we compare the performances of the :class:`~openturns.experimental.LatentVariableModel`
# with a naive approach, which would consist in modeling each combination of categorical
# variables through a separate and independent Gaussian process.

# %%
# In order to deal with mixed continuous / categorical problems we can rely on the
# :class:`~openturns.ProductCovarianceModel` class. We start here by defining the product kernel,
# which combines :class:`~openturns.SquaredExponential` kernels for the continuous variables, and
# :class:`~openturns.experimental.LatentVariableModel` for the categorical ones.

# %%
kx = ot.MaternModel()
kx.setNu(2.5) # smoothess
kz = otexp.LatentVariableModel(2, 1) # 2 categories in a 1D latent space
kLV = ot.ProductCovarianceModel([kx, kz])

# Bounds for the hyperparameter optimization
param_number = kLV.getParameter().getSize() - 1 # -1 because kz amplitude is fixed
lowerBoundLV = [1e-4] * param_number
upperBoundLV = [2.0] * param_number
boundsLV = ot.Interval(lowerBoundLV, upperBoundLV)

# Distribution for the hyperparameters initialization
unif_coll = [ot.Uniform(lowerBoundLV[i], upperBoundLV[i]) for i in range(param_number)]
initDistLV = ot.ComposedDistribution(unif_coll)

# %%
# As a reference, we consider a purely continuous kernel for independent Gaussian processes.
# One for each combination of categorical variables levels.

# %%
kIndependent = ot.SquaredExponential(1)
lowerBoundInd = [1e-4]
upperBoundInd = [20.0]
boundsInd = ot.Interval(lowerBoundInd, upperBoundInd)
initDistInd = ot.DistributionCollection()
for i in range(len(lowerBoundInd)):
    initDistInd.add(ot.Uniform(lowerBoundInd[i], upperBoundInd[i]))
initDistInd = ot.ComposedDistribution(initDistInd)
initSampleInd = initDistInd.getSample(10)
optAlgInd = ot.MultiStart(ot.NLopt("LN_COBYLA"), initSampleInd)

# %%
# Generate the training data set
x = dist.getSample(10)
y = fun(x)

# And the plotting data set
xPlt = dist.getSample(200)
xPlt = xPlt.sort()
yPlt = fun(xPlt)

# %%
# Initialize  and parameterize the optimization algorithm
initSampleLV = initDistLV.getSample(30)
optAlgLV = ot.MultiStart(ot.NLopt("LN_COBYLA"), initSampleLV)

# %%
# Create and train the Gaussian process models
algoLV = ot.KrigingAlgorithm(x, y, kLV)
algoLV.setOptimizationAlgorithm(optAlgLV)
algoLV.setOptimizationBounds(boundsLV)
algoLV.run()
resLV = algoLV.getResult()

algoIndependentList = []
for z in range(2):
    # Select the training samples corresponding to the correct combination
    # of categorical levels
    ind = np.where(np.all(np.array(x[:, 1]) == z, axis=1))[0]
    xLoc = x[ind][:, 0]
    yLoc = y[ind]

    # Create and train the Gaussian process models
    basis = ot.ConstantBasisFactory(1).build()
    algoIndependent = ot.KrigingAlgorithm(xLoc, yLoc, kIndependent)
    algoIndependent.setOptimizationAlgorithm(optAlgInd)
    algoIndependent.setOptimizationBounds(boundsInd)
    algoIndependent.run()
    algoIndependentList.append(algoIndependent.getResult())

# %%
# Plot the prediction of the mixed continuous / categorical GP,
# as well as the one of the two separate continuous GPs
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(15, 10))
for z in range(numberOfZLevels):
    # Select the training samples corresponding to the correct combination
    # of categorical levels
    ind = np.where(np.all(np.array(x[:, 1]) == z, axis=1))[0]
    xLoc = x[ind][:, 0]
    yLoc = y[ind]

    # Compute the models predictive performances on a validation data set.
    # The predictions are computed independently for each level of z,
    # i.e., by only considering the values of z corresponding to the
    # target level.
    ind = np.where(np.all(np.array(xPlt[:, 1]) == z, axis=1))[0]
    xPltInd = xPlt[ind]
    yPltInd = yPlt[ind]

    predMeanLV = resLV.getConditionalMean(xPltInd)
    predMeanInd = algoIndependentList[z].getConditionalMean(xPltInd[:, 0])
    predSTDLV = np.sqrt(resLV.getConditionalMarginalVariance(xPltInd))
    predSTDInd = np.sqrt(
        algoIndependentList[z].getConditionalMarginalVariance(xPltInd[:, 0])
    )

    (trainingData,) = ax1.plot(xLoc[:, 0], yLoc, "r*")
    (trueFunction,) = ax1.plot(xPltInd[:, 0], yPltInd, "k--")
    (prediction,) = ax1.plot(xPltInd[:, 0], predMeanLV, "b-")
    stdPred = ax1.fill_between(
        xPltInd[:, 0].asPoint(),
        (predMeanLV - predSTDLV).asPoint(),
        (predMeanLV + predSTDLV).asPoint(),
        alpha=0.5,
        color="blue",
    )
    ax2.plot(xLoc[:, 0], yLoc, "r*")
    ax2.plot(xPltInd[:, 0], yPltInd, "k--")
    ax2.plot(xPltInd[:, 0], predMeanInd, "b-")
    ax2.fill_between(
        xPltInd[:, 0].asPoint(),
        (predMeanInd - predSTDInd).asPoint(),
        (predMeanInd + predSTDInd).asPoint(),
        alpha=0.5,
        color="blue",
    )
ax1.legend(
    [trainingData, trueFunction, prediction, stdPred],
    ["Training data", "True function", "Prediction", "Prediction standard deviation"],
)
ax1.set_title("Mixed continuous-categorical modeling")
ax2.set_title("Separate modeling")
ax2.set_xlabel("x", fontsize=15)
ax1.set_ylabel("y", fontsize=15)
ax2.set_ylabel("y", fontsize=15)

fig.savefig("../figures/latent_variable_model.pdf", bbox_inches='tight')

