# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# %%
import openturns as ot
import numpy as np

def free_fall(X):
    g  = 9.81
    z0,v0,m,c = X
    tau=m/c
    vinf=-m*g/c
    t = np.array(mesh.getVertices().asPoint())
    z=z0+vinf*t+tau*(v0-vinf)*(1-np.exp(-t/tau))
    z=np.maximum(z,0.0)
    return ot.Field(mesh, z.reshape(-1, 1))

tmin=0. 
tmax=12.
gridsize=100 
mesh = ot.IntervalMesher([gridsize-1]).build(
ot.Interval(tmin, tmax))

alti = ot.PythonPointToFieldFunction(4, mesh,  1, free_fall)

distZ0 = ot.Uniform(50.0, 200.0)
distV0 = ot.Normal(55.0, 10.0)
distM = ot.Normal(80.0, 8.0)
distC = ot.Uniform(0.0, 30.0)
distX = ot.ComposedDistribution([distZ0, distV0,
 distM, distC])

size = 100
inputSample = distX.getSample(size)
outputField = alti(inputSample)



# %%
# Draw
from openturns.viewer import View

graph = outputField.draw().getGraph(0,0)
graph.setTitle("Free fall in viscous fluid")
graph.setXTitle("t")
graph.setYTitle("z")
v= View(graph)
v.save("trajectories.pdf")
v.save("trajectories.png")

# %%

meanField = outputField.computeMean()
meanFunction = ot.P1LagrangeEvaluation(
	meanField)
trend = ot.TrendTransform(meanFunction, mesh)
invTrend = trend.getInverse()
outputFieldCentered = invTrend(outputField)

truncThreshold = 1.0e-5
algo = ot.KarhunenLoeveSVDAlgorithm( 
	outputFieldCentered, truncThreshold)
algo.run()
KLResult = algo.getResult()

eigenValues = KLResult.getEigenvalues()

# %%
# Graphical
import matplotlib.pyplot as plt

plt.plot(eigenValues)
plt.semilogy()
plt.xlabel("k")
plt.ylabel("$\lambda_k$")
plt.title("Fredholm problem eigenvalues")
plt.grid("both")

# %%

scaledModes = KLResult.getScaledModesAsProcessSample()
graph = scaledModes.drawMarginal(0)
graph.setTitle('Modes de KL, chute visqueuse')
graph.setXTitle(r'$t$')
graph.setYTitle(r'$\varphi_k$')
leg = ot.Description([ 'Mode '+str(i +1) for
	 i in range(eigenValues.getDimension()) ])
graph.setLegends(leg)
graph.setLegendPosition('topleft')
view=View(graph)

# %%

projectionFunction = ot.KarhunenLoeveProjection(KLResult)
sampleKsi = projectionFunction(outputFieldCentered)
sampleKsi = sampleKsi[:,:2]
cloud = ot.Cloud(sampleKsi)
graph = ot.Graph("Trajectories in the reduced space", "$\\xi_1$", "$\\xi_2$", True)
graph.add(cloud)
v= View(graph)
v.save("Reduced_Space.pdf")

# %%
ot.ResourceMap.SetAsString("Contour-DefaultColorMap", "viridis")
ot.ResourceMap.SetAsBool("Contour-DefaultIsFilled", True)
ot.ResourceMap.SetAsUnsignedInteger("Contour-DefaultLevelsNumber", 15)


cov = KLResult.getCovarianceModel()

# As a covariance function
isStationary = False
asCorrelation = False
graph = cov.draw(0, 0, tmin, tmax, 128, isStationary, asCorrelation)
graph.setTitle("Viscous free fall covariance")
v = View(graph)#, contour_kw={"levels": 50})
v.save("Covariance.pdf")

# %%

# As a correlation function
asCorrelation = True
graph = cov.draw(0, 0, tmin, tmax, 128, isStationary, asCorrelation)
graph.setTitle("Viscous free fall correlation")
v = View(graph)#, contour_kw={"levels": 50})
v.save("Correlation.pdf")

# %%
# Copulas


R = ot.CorrelationMatrix(2)
R[1, 0] = 0.2
c = ot.NormalCopula(R).drawPDF()
c.setTitle("Normal copula")
v = View(c, contour_kw={"vmin": 0.4, "vmax": 1.4})
v.save("Copula1.pdf")

# %%

c = ot.ClaytonCopula().drawPDF()
c.setTitle("Clayton copula")
v = View(c, contour_kw={"vmin": 0.0, "vmax": 2.6})
v.save("Copula2.pdf")

# %%


c = ot.AliMikhailHaqCopula().drawPDF()
c.setTitle("AliMikhailHaq copula")
v = View(c, contour_kw={"vmin": 0.5, "vmax": 1.4})
v.save("Copula3.pdf")

# %%

c = ot.GumbelCopula().drawPDF()
c.setTitle("Gumbel copula")
v = View(c, contour_kw={"vmin": 0.0, "vmax": 2.6})
v.save("Copula4.pdf")

# %%

marg1 = ot.Gumbel(1.0, 0.0)
marg2 = ot.TruncatedNormal(0.0, 1.0, -2.0, 2.0)
joint = ot.JointDistribution([marg1, marg2])
g = joint.drawPDF()
v = View(g, contour_kw={"vmin": 0.0, "vmax": 0.13})
v.save("Dist.pdf")

# %%
marg1 = ot.Gumbel(1.0, 0.0)
marg2 = ot.TruncatedNormal(0.0, 1.0, -2.0, 2.0)
copula = ot.GumbelCopula()
joint = ot.JointDistribution([marg1, marg2], copula)
graph = joint.drawPDF()
title = "Joint distribution "
title += "from marginals and copula"
graph.setTitle(title)
v = View(graph)
v.save("ComposedGumbel.pdf")

# %%
