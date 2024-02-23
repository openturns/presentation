"""
Estimate Sobol indices on a field to point function
===================================================
"""

# %%
# In this example, we are going to perform sensitivity analysis of an application that takes
# fields as input and vectors as output from a sample of data:
#
# .. math::
#     h: \left|
#       \begin{array}{ccl}
#          \cM_N \times (\Rset^d)^N & \rightarrow & \Rset^p \\
#          \mat{X} & \mapsto & \vect{Y}
#       \end{array}
#     \right.
#
# This involves these steps:
#
# - Generate some input/output data matching the application :math:`h`
# - Run the :class:`~openturns.experimental.FieldToPointFunctionalChaosAlgorithm` class
# - Validate the Karhunen-Loeve decompositions of the inputs
# - Validate the chaos metamodel between the KL coefficients and the outputs
# - Retrieve the Sobol' indices from :class:`~openturns.FieldFunctionalChaosSobolIndices`
#

# %%
import openturns as ot
import openturns.experimental as otexp
from openturns.viewer import View
import matplotlib.pyplot as plt
import numpy as np


# %%
# First build a process to generate the input data.
# We assemble a 4-d process from functional and Gaussian processes.
T = 3.0
NT = 32
tg = ot.RegularGrid(0.0, T / NT, NT)
f1 = ot.SymbolicFunction(["t"], ["sin(t)"])
f2 = ot.SymbolicFunction(["t"], ["cos(t)^2"])
coeff1_dist = ot.Normal([1.0] * 2, [0.6] * 2, ot.CorrelationMatrix(2))
p1 = ot.FunctionalBasisProcess(coeff1_dist, ot.Basis([f1, f2]), tg)
p2 = ot.GaussianProcess(ot.SquaredExponential([1.0], [T / 4.0]), tg)
coeff3_dist = ot.ComposedDistribution([ot.Uniform(), ot.Normal()])
f1 = ot.SymbolicFunction(["t"], ["1"])
f2 = ot.SymbolicFunction(["t"], ["t"])
p3 = ot.FunctionalBasisProcess(coeff3_dist, ot.Basis([f1, f2]))
X = ot.AggregatedProcess([p1, p2, p3])
X.setMesh(tg)

# %%
# Draw some input trajectories from our process
ot.RandomGenerator.SetSeed(0)
x = X.getSample(10)
grid = ot.GridLayout(3, 1)
for i in range(3):
    graph = x.drawMarginal(i)
    graph.setTitle("Trajectories of dimension #{}".format(i))
    grid.setGraph(i, 0, graph)
v = View(grid)
v.save("../figures/time_series.pdf")
# %%
trajectories_3d = []
for i in range(x.getSize()): # i=0..9
    trajectory = ot.Sample(x.getTimeGrid().getN(), x.getDimension())
    for j in range(x.getDimension()): #j = 0 1 2
        marginal = x.getMarginal(j)
        field = marginal.getField(i)
        trajectory[:, j] = field.getValues()
    trajectories_3d.append(trajectory)
    
trajectory_0 = trajectories_3d[0]

# Draw 3d scatter plot
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.set_xlabel('Dimension #0')
ax.set_ylabel('Dimension #1')
ax.set_zlabel('Dimension #2')

# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
for trajectory in trajectories_3d:
    xs = trajectory.getMarginal(0)
    ys = trajectory.getMarginal(1)
    zs = trajectory.getMarginal(2)
    ax.scatter(xs, ys, zs, marker='+')
ax.set_title(r'$f \in \mathcal{F}([0,3], \mathbb{R}^3)$')
plt.savefig("../figures/scatter_3d.pdf", bbox_inches='tight')
plt.show()

# %%
# Generate input realizations and the corresponding output from a Field->Point function


class pyf2p(ot.OpenTURNSPythonFieldToPointFunction):
    def __init__(self, mesh):
        super(pyf2p, self).__init__(mesh, 3, 1)
        self.setInputDescription(["x1", "x2", "x3"])
        self.setOutputDescription(["y"])

    def _exec(self, X):
        Xs = ot.Sample(X)
        x1, x2, x3 = Xs.computeMean()
        y = x1 + x2 - x3 + x1 * x3 - 0.1 * x1 * x2 * x3
        return [y]


f = ot.FieldToPointFunction(pyf2p(tg))
y_trajectories = f(x)

# Draw 3d scatter plot
fig,ax  = plt.subplots(1, 1, figsize=(2,5))
for y_point in y_trajectories:
    ax.scatter([0.0], y_point)
ax.set_xticklabels("")
ax.yaxis.tick_right()
ax.set_title("$h(f) \in \mathbb{R}$")
fig.savefig("../figures/response.pdf", bbox_inches='tight')
# %%
N = 1000
x = X.getSample(N)
y = f(x)

# %%
# Run the field-vector algorithm that performs KL-decomposition of the inputs
# and chaos learning between the KL coefficients and the output vectors
algo = otexp.FieldToPointFunctionalChaosAlgorithm(x, y)
# 1. KL parameters
#algo.setCenteredSample(False)  # our input sample is not centered (default)
algo.setThreshold(4e-2)  # we expect to explain 96% of variance
# algo.setRecompress(
#     False
# )  # whether to re-truncate modes according to a global eigen value threshold across inputs (default)
#algo.setNbModes(10)  # max KL modes (default=unlimited)
# 2. chaos parameters:
# bs = ot.ResourceMap.GetAsUnsignedInteger("FunctionalChaosAlgorithm-BasisSize")
# ot.ResourceMap.SetAsUnsignedInteger(
#     "FunctionalChaosAlgorithm-BasisSize", N
# )  # chaos basis size
# ot.ResourceMap.SetAsBool("FunctionalChaosAlgorithm-Sparse", True)
algo.run()
#ot.ResourceMap.SetAsUnsignedInteger("FunctionalChaosAlgorithm-BasisSize", bs)
result = algo.getResult()

# %%
# Retrieve the eigen values of each KL decomposition:
# we observe that each input process is represented by a different number of modes.
pca_collection = result.getInputKLResultCollection()
d=len(pca_collection)
grid = ot.GridLayout(1, d)
for num, pca in enumerate(pca_collection):
    graph = pca.getModesAsProcessSample().drawMarginal(0)
    graph.setTitle(f"Dimension #{num}")
    grid.setGraph(0, num, graph)

v = View(grid)
v.save("../figures/pca_modes.pdf")

# %%
# Validation of the PCA

grid = ot.GridLayout(1, d)
for num, pca in enumerate(pca_collection):
    m = x.getMarginal(num)
    v = ot.KarhunenLoeveValidation(m, pca)
    graph=v.drawValidation().getGraph(0,0)
    ratio = 100.0 * pca.getSelectionRatio()
    graph.setTitle(f"Ratio = {ratio:.2f}%")
    grid.setGraph(0, num, graph)

v = View(grid)
v.save("../figures/pca_validation.png")


# %%
# Inspect the chaos quality: residuals and relative errors.
# The relative error is very low; that means the chaos decomposition performs very well.
print(f"residuals={result.getFCEResult().getResiduals()}")
print(f"relative errors={result.getFCEResult().getRelativeErrors()}")

# %%
# Graphically validate the chaos result:
# we can see the points are very close to the diagonal; this means
# approximated points are very close to the learning points.
modes = result.getModesSample()
metamodel = result.getFCEResult().getMetaModel()
output = result.getOutputSample()
#validation = ot.MetaModelValidation(modes, output, metamodel)
validation = ot.MetaModelValidation(modes, output, metamodel)
q2 = validation.computePredictivityFactor()
print(f"q2={q2}")
graph = validation.drawValidation()
graph.setTitle(f"Chaos validation - q2={q2}")
_ = View(graph)

# %%
fig = plt.figure(figsize=(12, 12))
lowerBound = modes.getMin()
upperBound = modes.getMax()

# Definition of number of meshes in x and y axes for the 2D cross cut plots
nX = 20
nY = 20
for i in range(6):
    for j in range(i):
        crossCutIndices = []
        crossCutReferencePoint = []
        for k in range(6):
            if k != i and k != j:
                crossCutIndices.append(k)
                # Definition of the reference point
                crossCutReferencePoint.append(modes.computeMean()[k])
        # Definition of 2D cross cut function
        crossCutFunction = ot.ParametricFunction(
            metamodel, crossCutIndices, crossCutReferencePoint
        )
        crossCutLowerBound = [lowerBound[j], lowerBound[i]]
        crossCutUpperBound = [upperBound[j], upperBound[i]]
        # Definition of the mesh
        inputData = ot.Box([nX, nY]).generate()
        inputData *= ot.Point(crossCutUpperBound) - ot.Point(crossCutLowerBound)
        inputData += ot.Point(crossCutLowerBound)
        meshX = np.array(inputData)[:, 0].reshape(nX + 2, nY + 2)
        meshY = np.array(inputData)[:, 1].reshape(nX + 2, nY + 2)
        data = crossCutFunction(inputData)
        meshZ = np.array(data).reshape(nX + 2, nY + 2)
        levels = [(150 + 3 * i) for i in range(101)]

        # Creation of the contour
        index = 1 + i * 6 + j

        ax = fig.add_subplot(6, 6, index)
        ax.pcolormesh(
            meshX, meshY, meshZ, cmap="viridis", shading="auto"
        )
        ax.set_xticks([])
        ax.set_yticks([])

# %%
# Perform an evaluation on a new realization and ensure the output
# is close to the evaluation with the reference function
metamodel = result.getFieldToPointMetamodel()
x0 = X.getRealization()
y0 = f(x0)
y0hat = metamodel(x0)
print(f"y0={y0} y0^={y0hat}")

# %%
ot.RandomGenerator.SetSeed(1)
x_valid = X.getSample(100)
y_valid = f(x_valid)
yhat_valid = metamodel(x_valid)
graph = ot.VisualTest.DrawQQplot(y_valid, yhat_valid) # graphical validation
graph.setTitle("")
graph.setXTitle("True output values")
graph.setYTitle("Surrogate model values")
v = View(graph)
v.save("../figures/validation.pdf")
# %%
# Retrieve the first order Sobol' indices
# The preponderant variables are x2, x4 whereas x1, x3 have a low influence on the output
sensitivity = otexp.FieldFunctionalChaosSobolIndices(result)
sobol_0 = sensitivity.getFirstOrderIndices()
print(f"first order={sobol_0}")

# %%
# Retrieve the total Sorder obol' indices
# The x3,x4 variables have total order indices significantly different than
# their first order indices counterpart meaning they interact with other variables
sobol_0t = sensitivity.getTotalOrderIndices()
print(f"total order={sobol_0t}")

# %%
# Draw the Sobol' indices
graph = sensitivity.draw()
view = View(graph)
view.save("../figures/sobol.pdf")

View.ShowAll()

# %%
# Reset default settings
ot.ResourceMap.Reload()

# %%
