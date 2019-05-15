from openturns import *
from openturns.viewer import *

# General 1D
distribution = Mixture(DistributionCollection([UserDefined(Sample(1, 1)), Uniform(0.0, 1.0)]))
distribution.setName("1D general random vector")
distribution.setDescription(Description(["X"]))
view = View(distribution.drawCDF(512))
view.save("GeneralCDF1D.pdf")
view.close()

# General 2D
sample = Normal(2).getSample(10)
xMin = sample.getMin()
xMax = sample.getMax()
delta = (xMax + (xMin * (-1.0))) * 0.1
distribution = Mixture(DistributionCollection([UserDefined(sample), Normal(Point([-1.5, -2.0]), Point([2.0, 1.5]), CorrelationMatrix(2))]))
distribution.setName("2D general random vector")
distribution.setDescription(Description(["X_1", "X_2"]))
view = View(distribution.drawCDF(Point([-5, -5]), Point([5, 5]), [512]*2), square_axes=True)
view.save("GeneralCDF2D.pdf")
view.close()

# Continuous 1D
distribution = Mixture(DistributionCollection([Normal(-1.0, 1.0), Normal(4.0, 1.5)]))
distribution.setName("1D continuous random vector")
distribution.setDescription(Description(["X"]))
view = View(distribution.drawPDF(512))
view.save("ContinuousPDF1D.pdf")
view.close()
view = View(distribution.drawCDF(512))
view.save("ContinuousCDF1D.pdf")
view.close()

# Continuous 2D
distribution = Mixture(DistributionCollection([Normal(Point([-1.0, 1.0]), Point([1.0, 1.0]), CorrelationMatrix(2)), Normal(Point([-1.5, -2.0]), Point([2.0, 1.5]), CorrelationMatrix(2)), Normal(Point([2.5, 0.5]), Point([1.5, 0.5]), CorrelationMatrix(2))]))
distribution.setName("2D continuous random vector")
distribution.setDescription(Description(["X_1", "X_2"]))
view = View(distribution.drawPDF([-8.0, -6.0], [8.0, 10.0], [512]*2), square_axes=True)
view.save("ContinuousPDF2D.pdf")
view.close()
view = View(distribution.drawCDF([-8.0, -6.0], [8.0, 10.0], [512]*2), square_axes=True)
view.save("ContinuousCDF2D.pdf")
view.close()

# Discrete 1D
tmpDistribution = Mixture(DistributionCollection([Binomial(10, 0.15), Binomial(15, 0.6)]))
points = Sample(0,1)
weights = Point(0)
for i in range(16):
    weights.add(tmpDistribution.computePDF(i))
    points.add(Point(1, i))
distribution = UserDefined(points, weights)
distribution.setName("1D discrete random vector")
distribution.setDescription(Description(["X"]))
view = View(distribution.drawPDF(-3.0, 20.0))
view.save("DiscretePDF1D.pdf")
view.close()
view = View(distribution.drawCDF(-3.0, 20.0))
view.save("DiscreteCDF1D.pdf")
view.close()

# Discrete 2D
sample = Normal(2).getSample(10)
xMin = sample.getMin()
xMax = sample.getMax()
delta = (xMax + (xMin * (-1.0))) * 0.1
u = xMin - delta
v = xMax + delta
a = [min(u[0], u[1])]*2
b = [max(v[0], v[1])]*2
distribution = UserDefined([[0.2 * int(5 * x[0]), 0.2 * int(5 * x[1])] for x in sample], RandomGenerator.Generate(10))
distribution.setName("2D discrete random vector")
distribution.setDescription(Description(["X_1", "X_2"]))
view = View(distribution.drawPDF(a, b), square_axes=True)
view.save("DiscretePDF2D.pdf")
view.close()
view = View(distribution.drawCDF(a, b), square_axes=True)
view.save("DiscreteCDF2D.pdf")
view.close()
