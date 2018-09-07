from openturns import *

# General 1D
distribution = Mixture(DistributionCollection([UserDefined(NumericalSample(1, 1)), Uniform(0.0, 1.0)]))
distribution.setName("1D general random vector")
distribution.setDescription(Description(["X"]))
distribution.drawCDF().draw("GeneralCDF1D")

# General 2D
sample = Normal(2).getNumericalSample(10)
xMin = sample.getMin()
xMax = sample.getMax()
delta = (xMax + (xMin * (-1.0))) * 0.1
distribution = Mixture(DistributionCollection([UserDefined(sample), Normal(NumericalPoint([-1.5, -2.0]), NumericalPoint([2.0, 1.5]), CorrelationMatrix(2))]))
distribution.setName("2D general random vector")
distribution.setDescription(Description(["X_1", "X_2"]))
distribution.drawCDF(NumericalPoint([-5, -5]), NumericalPoint([5, 5])).draw("GeneralCDF2D")

# Continuous 1D
distribution = Mixture(DistributionCollection([Normal(-1.0, 1.0), Normal(4.0, 1.5)]))
distribution.setName("1D continuous random vector")
distribution.setDescription(Description(["X"]))
distribution.drawPDF().draw("ContinuousPDF1D")
distribution.drawCDF().draw("ContinuousCDF1D")

# Continuous 2D
distribution = Mixture(DistributionCollection([Normal(NumericalPoint([-1.0, 1.0]), NumericalPoint([1.0, 1.0]), CorrelationMatrix(2)), Normal(NumericalPoint([-1.5, -2.0]), NumericalPoint([2.0, 1.5]), CorrelationMatrix(2)), Normal(NumericalPoint([2.5, 0.5]), NumericalPoint([1.5, 0.5]), CorrelationMatrix(2))]))
distribution.setName("2D continuous random vector")
distribution.setDescription(Description(["X_1", "X_2"]))
distribution.drawPDF().draw("ContinuousPDF2D")
distribution.drawCDF().draw("ContinuousCDF2D")

# Discrete 1D
tmpDistribution = Mixture(DistributionCollection([Binomial(10, 0.15), Binomial(15, 0.6)]))
collection = UserDefinedPairCollection(0)
for i in range(16):
    collection.add(UserDefinedPair(NumericalPoint(1, i), tmpDistribution.computePDF(i)))
distribution = UserDefined(collection)
distribution.setName("1D discrete random vector")
distribution.setDescription(Description(["X"]))
distribution.drawPDF(-3.0, 20.0).draw("DiscretePDF1D")
distribution.drawCDF(-3.0, 20.0).draw("DiscreteCDF1D")

# Discrete 2D
sample = Normal(2).getNumericalSample(10)
xMin = sample.getMin()
xMax = sample.getMax()
delta = (xMax + (xMin * (-1.0))) * 0.1
distribution = UserDefined(sample)
distribution.setName("2D discrete random vector")
distribution.setDescription(Description(["X_1", "X_2"]))
distribution.drawCDF(xMin + (delta * (-1.0)), xMax + delta).draw("DiscreteCDF2D")
