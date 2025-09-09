"""
Conditional expectation of a polynomial chaos expansion
=======================================================

This script is adapted from the example, but produces a better picture for slides.
"""

# %%
import openturns as ot
import openturns.viewer as otv
from openturns.usecases import ishigami_function
import matplotlib.pyplot as plt

# %%
# The next function creates a parametric PCE based on a
# given PCE and a set of indices.


# %%
def meanParametricPCE(chaosResult, indices):
    """
    Return the parametric PCE of Y with given input marginals set to the mean.

    All marginal inputs, except those in the conditioning indices
    are set to the mean of the input random vector.

    The resulting function is :

    g(xu) = PCE(xu, xnotu = E[Xnotu])

    where xu is the input vector of conditioning indices,
    xnotu is the input vector fixed indices and
    E[Xnotu] is the expectation of the random vector of the components
    not in u.

    Parameters
    ----------
    chaosResult: ot.FunctionalChaosResult(inputDimension)
        The polynomial chaos expansion.
    indices: ot.Indices()
        The indices of the input variables which are set to constant values.

    Returns
    -------
    parametricPCEFunction : ot.ParametricFunction(reducedInputDimension, outputDimension)
        The parametric PCE.
        The reducedInputDimension is equal to inputDimension - indices.getSize().
    """
    inputDistribution = chaosResult.getDistribution()
    if not inputDistribution.hasIndependentCopula():
        raise ValueError(
            "The input distribution has a copula" "which is not independent"
        )
    # Create the parametric function
    pceFunction = chaosResult.getMetaModel()
    xMean = inputDistribution.getMean()
    referencePoint = xMean[indices]
    parametricPCEFunction = ot.ParametricFunction(pceFunction, indices, referencePoint)
    return parametricPCEFunction


# %%
# The next function creates a sparse PCE using least squares.


# %%
def computeSparseLeastSquaresFunctionalChaos(
    inputTrain,
    outputTrain,
    multivariateBasis,
    basisSize,
    distribution,
    sparse=True,
):
    """
    Create a sparse polynomial chaos based on least squares.

    * Uses the enumerate rule in multivariateBasis.
    * Uses the LeastSquaresStrategy to compute the coefficients based on
      least squares.
    * Uses LeastSquaresMetaModelSelectionFactory to use the LARS selection method.
    * Uses FixedStrategy in order to keep all the coefficients that the
      LARS method selected.

    Parameters
    ----------
    inputTrain : ot.Sample
        The input design of experiments.
    outputTrain : ot.Sample
        The output design of experiments.
    multivariateBasis : ot.Basis
        The multivariate chaos basis.
    basisSize : int
        The size of the function basis.
    distribution : ot.Distribution.
        The distribution of the input variable.
    sparse: bool
        If True, create a sparse PCE.

    Returns
    -------
    result : ot.PolynomialChaosResult
        The estimated polynomial chaos.
    """
    if sparse:
        selectionAlgorithm = ot.LeastSquaresMetaModelSelectionFactory()
    else:
        selectionAlgorithm = ot.PenalizedLeastSquaresAlgorithmFactory()
    projectionStrategy = ot.LeastSquaresStrategy(
        inputTrain, outputTrain, selectionAlgorithm
    )
    adaptiveStrategy = ot.FixedStrategy(multivariateBasis, basisSize)
    chaosAlgorithm = ot.FunctionalChaosAlgorithm(
        inputTrain, outputTrain, distribution, adaptiveStrategy, projectionStrategy
    )
    chaosAlgorithm.run()
    chaosResult = chaosAlgorithm.getResult()
    return chaosResult


# %%
# In the next cell, we create a training sample from the
# Ishigami test function.
# We choose a sample size equal to 1000.

# %%
ot.Log.Show(ot.Log.NONE)
ot.RandomGenerator.SetSeed(0)
im = ishigami_function.IshigamiModel()
input_names = im.inputDistribution.getDescription()
sampleSize = 1000
inputSample = im.inputDistribution.getSample(sampleSize)
outputSample = im.model(inputSample)


# %%
# We then create a sparce PCE of the Ishigami function using
# a candidate basis up to the total degree equal to 12.
# This leads to 455 candidate coefficients.
# The coefficients are computed from least squares.

# %%
multivariateBasis = ot.OrthogonalProductPolynomialFactory([im.X1, im.X2, im.X3])
totalDegree = 12
enumerateFunction = multivariateBasis.getEnumerateFunction()
basisSize = enumerateFunction.getBasisSizeFromTotalDegree(totalDegree)
print("Basis size = ", basisSize)

# %%
# Finally, we create the PCE.
# Only 61 coefficients are selected by the :class:`~openturns.LARS`
# algorithm.

# %%
chaosResult = computeSparseLeastSquaresFunctionalChaos(
    inputSample,
    outputSample,
    multivariateBasis,
    basisSize,
    im.inputDistribution,
)
print("Selected basis size = ", chaosResult.getIndices().getSize())
chaosResult


# %%
# In order to see the structure of the data, we create a grid of
# plots which shows all projections of :math:`Y` versus :math:`X_i`
# for :math:`i = 1, 2, 3`.
# We see that the Ishigami function is particularly non linear.

# %%
grid = ot.VisualTest.DrawPairsXY(inputSample, outputSample)
grid.setTitle(f"n = {sampleSize}")
view = otv.View(grid, figure_kw={"figsize": (8.0, 3.0)})
plt.subplots_adjust(wspace=0.4, bottom=0.25)

# %%
# Parametric function
# ~~~~~~~~~~~~~~~~~~~
#
# We now create the parametric function where :math:`X_i` is free
# and the other variables are set to their mean values.
# We can show that a parametric PCE is, again, a PCE.
# The library does not currently implement this feature.
# In the next cell, we create it from the `meanParametricPCE` we defined
# previously.

# %%
# Create different parametric functions for the PCE.
# In the next cell, we create the parametric PCE function
# where :math:`X_1` is active while :math:`X_2` and :math:`X_3` are
# set to their mean values.
indices = [1, 2]
parametricPCEFunction = meanParametricPCE(chaosResult, indices)
print(parametricPCEFunction.getInputDimension())


# %%
# Now that we know how the `meanParametricPCE` works, we loop over
# the input marginal indices and consider the three functions
# :math:`\widehat{\model}_1(\inputReal_1)`,
# :math:`\widehat{\model}_2(\inputReal_2)` and
# :math:`\widehat{\model}_3(\inputReal_3)`.
# For each marginal index `i`, we we plot the output :math:`Y`
# against the input marginal :math:`X_i` of the sample.
# Then we plot the parametric function depending on :math:`X_i`.

# %%
inputDimension = im.inputDistribution.getDimension()
npPoints = 100
inputRange = im.inputDistribution.getRange()
inputLowerBound = inputRange.getLowerBound()
inputUpperBound = inputRange.getUpperBound()
# Create the palette with transparency
palette = ot.Drawable().BuildDefaultPalette(2)
firstColor = palette[0]
r, g, b, a = ot.Drawable.ConvertToRGBA(firstColor)
newAlpha = 64
newColor = ot.Drawable.ConvertFromRGBA(r, g, b, newAlpha)
palette[0] = newColor
grid = ot.VisualTest.DrawPairsXY(inputSample, outputSample)
reducedBasisSize = chaosResult.getCoefficients().getSize()
# grid.setTitle(
#     f"n = {sampleSize}, total degree = {totalDegree}, "
#     f"basis = {basisSize}, selected = {reducedBasisSize}"
# )
for i in range(inputDimension):
    graph = grid.getGraph(0, i)
    graph.setLegends(["Data"])
    graph.setXTitle(f"$x_{1 + i}$")
    graph.setYTitle("y")
    graph.setTickLocation(2)
    # Set all indices except i
    indices = list(range(inputDimension))
    indices.pop(i)
    parametricPCEFunction = meanParametricPCE(chaosResult, indices)
    xiMin = inputLowerBound[i]
    xiMax = inputUpperBound[i]
    curve = parametricPCEFunction.draw(xiMin, xiMax, npPoints).getDrawable(0)
    curve.setLineWidth(2.0)
    curve.setLegend(r"$PCE(x_i, x_{-i} = \mathbb{E}[X_{-i}])$")
    graph.add(curve)
    if i < inputDimension - 1:
        graph.setLegends([""])
    else:
        graph.setLegends(["", r"$PCE(x_i, x_{-i} = \mathbb{E}[X_{-i}])$"])
    graph.setColors(palette)
    grid.setGraph(0, i, graph)

grid.setLayout(3, 1)
# graph = grid.getGraph(1, 1)
# graph.add(ot.Cloud([[0.0, 0.0]]))
# graph.add(ot.Curve([[0.0]], [[0.0]]))
# #graph.setLegends(["Data", r"$PCE(x_i, x_{-i} = \mathbb{E}[X_{-i}])$"])
# graph.setLegendPosition("left")
# grid.setGraph(1, 1, graph)
grid.setLegendPosition("bottomright")

view = otv.View(
    grid,
    figure_kw={"figsize": (6.5, 6.5)},
    # legend_kw={"bbox_to_anchor": (-0.85, -0.6)},
)
view.save("pce_conditional.png")
# view = otv.View(grid)
# plt.subplots_adjust(wspace=0.4, right=0.7, bottom=0.6)
# plt.savefig("pce_conditional.png")
# %%
# We see that the parametric function is located within each cloud, but
# sometimes seems a little vertically on the edges of the data.
# More precisely, the function represents well how :math:`Y` depends
# on :math:`X_2`, but does not seem to represent well how :math:`Y`
# depends on :math:`X_1` or :math:`X_3`.

# %%
# Conditional expectation
# ~~~~~~~~~~~~~~~~~~~~~~~

# %%
# In the next cell, we create the conditional expectation function
# :math:`\Expect{\model(\inputReal) \; | \; \inputRV_1 = \inputReal_1}`.

# %%
conditionalPCE = chaosResult.getConditionalExpectation([0])
conditionalPCE

# %%
# On output, we see that the result is, again, a PCE.
# Moreover, a subset of the previous coefficients are presented in this
# conditional expectation: only multi-indices which involve
# :math:`X_1` are presented (and the other marginal components are removed).
# We observe that the value of the coefficients are unchanged with respect to the
# previous PCE.

# %%
# In the next cell, we create the conditional expectation function
# :math:`\Expect{\model(\inputReal) \; | \; \inputRV_2 = \inputReal_2, \inputRV_3 = \inputReal_3}`.

# %%
conditionalPCE = chaosResult.getConditionalExpectation([1, 2])
conditionalPCE

# %%
# We see that the conditional PCE has input dimension 2.


# %%
# In the next cell, we compare the parametric PCE and the conditional
# expectation of the PCE.

# sphinx_gallery_thumbnail_number = 3
inputDimension = im.inputDistribution.getDimension()
npPoints = 100
inputRange = im.inputDistribution.getRange()
inputLowerBound = inputRange.getLowerBound()
inputUpperBound = inputRange.getUpperBound()
# Create the palette with transparency
palette = ot.Drawable().BuildDefaultPalette(3)
firstColor = palette[0]
r, g, b, a = ot.Drawable.ConvertToRGBA(firstColor)
newAlpha = 64
newColor = ot.Drawable.ConvertFromRGBA(r, g, b, newAlpha)
palette[0] = newColor
grid = ot.VisualTest.DrawPairsXY(inputSample, outputSample)
grid.setTitle(f"n = {sampleSize}, total degree = {totalDegree}")
for i in range(inputDimension):
    graph = grid.getGraph(0, i)
    graph.setLegends(["Data"])
    graph.setXTitle(f"$x_{1 + i}$")
    xiMin = inputLowerBound[i]
    xiMax = inputUpperBound[i]
    # Set all indices except i to the mean
    indices = list(range(inputDimension))
    indices.pop(i)
    parametricPCEFunction = meanParametricPCE(chaosResult, indices)
    # Draw the parametric function
    curve = parametricPCEFunction.draw(xiMin, xiMax, npPoints).getDrawable(0)
    curve.setLineWidth(2.0)
    curve.setLineStyle("dashed")
    curve.setLegend(r"$PCE\left(x_i, x_{-i} = \mathbb{E}[X_{-i}]\right)$")
    graph.add(curve)
    # Compute conditional expectation given Xi
    conditionalPCE = chaosResult.getConditionalExpectation([i])
    print(f"i = {i}")
    print(conditionalPCE)
    conditionalPCEFunction = conditionalPCE.getMetaModel()
    curve = conditionalPCEFunction.draw(xiMin, xiMax, npPoints).getDrawable(0)
    curve.setLineWidth(2.0)
    curve.setLegend(r"$\mathbb{E}\left[PCE | X_i = x_i\right]$")
    graph.add(curve)
    if i < inputDimension - 1:
        graph.setLegends([""])
    graph.setColors(palette)
    # Set the graph into the grid
    grid.setGraph(0, i, graph)

grid.setLegendPosition("topright")
view = otv.View(
    grid,
    figure_kw={"figsize": (8.0, 3.0)},
    legend_kw={"bbox_to_anchor": (1.0, 1.0), "loc": "upper left"},
)
plt.subplots_adjust(wspace=0.4, right=0.7, bottom=0.25)

# %%
# We see that the conditional expectation of the PCE is a better
# approximation of the data set than the parametric PCE.

# %%
# Conclusion
# ~~~~~~~~~~
#
# In this example, we have seen how to compute the conditional
# expectation of a PCE.
# We have seen that this function is a good approximation of the Ishigami
# function when we reduce the input dimension.
# We have also seen that the parametric PCE might be a poor
# approximation of the Ishigami function.
# This is because the parametric PCE depends on the particular value
# that we have chosen to create the parametric function.
#
# The fact that the conditional expectation of the PCE is a
# good approximation of the function when we reduce the input dimension
# is a consequence of a theorem which states that the
# conditional expectation is the best approximation of the
# function in the least squares sense (see [girardin2018]_ page 79).

# %%
otv.View.ShowAll()
