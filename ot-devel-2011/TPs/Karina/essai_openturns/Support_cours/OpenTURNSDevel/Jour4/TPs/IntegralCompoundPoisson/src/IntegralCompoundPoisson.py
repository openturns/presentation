from openturns import *
from IntegralUserDefined import *
from Polynomial import *
from checkVersion import *
from cmath import *
from numpy import *

class IntegralCompoundPoisson(DistributionImplementation):
    def __init__(self, atomDistribution, theta,  log2cache = 10):
        DistributionImplementation.__init__(self)
        self.useNewOpenturns_ = isAfter(0, 13, 2)
        self.setName("IntegralCompoundPoisson")
        # Check the validity of d
        if atomDistribution.getClassName() != "IntegralUserDefined":
            raise Exception('In IntegralCompoundPoisson', 'the atom distribution must be an IntegralUserDefined distribution.')
        self.atomDistribution_ = atomDistribution
        # Check the validity of theta
        if theta <= 0.0:
                raise Exception('In IntegralCompoundPoisson', 'The Poisson parameter theta must be > 0.0')
        self.theta_ = theta
        self.poisson_ = Poisson(theta)
        # Build the Q polynomial
        q = UniVariatePolynomial(NumericalPoint(1, 0.0))
        # Get the information to build the generating function (GF) of the atom distribution as a sparse polynomial
        support = atomDistribution.getSupport()
        coeffs = atomDistribution.getNormalizedWeights() * theta
        # Substract theta
        support.add(0)
        coeffs.add(-theta)
        self.q_ = buildUniVariatePolynomial(support, coeffs)
        self.denseQCoefficients_ = self.q_.getCoefficients()
        self.pdfCache_ = NumericalPoint(0)
        self.cdfCache_ = NumericalPoint(0)
        self.log2Cache_ = log2cache
        self.m_ = 2**log2cache
        self.fillComputationCache()

    def fillComputationCache(self):
        self.r_ = 10.0 ** (-10.63 / (self.m_))
        GFCache  = NumericalComplexCollection(self.m_)
        self.expCache_ = NumericalComplexCollection(self.m_)
        self.rPowerCache_ = NumericalPoint(self.m_)
        # Initial value
        self.expCache_[0] = 1.0
        self.rPowerCache_[0] = 1.0
        for i in xrange(1, self.m_):
            self.expCache_[i] = exp(2.0j * pi * float(i) / self.m_)
            self.rPowerCache_[i] = self.rPowerCache_[i - 1] * self.r_
        # Poisson's inversion formula
        # p_n = 1/(mr^n)\sum_{k=0}^{m-1} G(r\exp(2i\pi k/m))\exp(-2i\pi n k / m)
        # FFT
        # X_k = \sum_{n=0}^{N-1}x_n\exp(-2i\pi kn/N), k=0..N-1
        for i in xrange(self.m_):
            GFCache[i] = exp(self.computeQ(i))
        X = fft.fft(GFCache)
        candidate = NumericalPoint(self.m_)
        for i in xrange(self.m_):
            candidate[i] = X[i].real / (self.m_ * self.rPowerCache_[i])
            # Due to roundoff errors, the computed pdf can be slightly negative
            if candidate[i] < 0.0:
                candidate[i] = 0.0
        self.pdfCache_ = candidate

    def computeQ(self, k):
        if self.useNewOpenturns_:
            return self.q_(self.r_ * self.expCache_[k])
        if k == 0.0:
            return self.computeQReal(self.r_)
        x = self.r_ * self.expCache_[k]
        size = self.denseQCoefficients_.getSize()
        val = self.denseQCoefficients_[size - 1]
        for i in xrange(size - 1, 0, -1):
            val = val * x + self.denseQCoefficients_[i - 1]
        return val

    def computeQReal(self, x):
        size = self.denseQCoefficients_.getSize()
        val = self.denseQCoefficients_[size - 1]
        for i in xrange(size - 1, 0, -1):
            val = val * x + self.denseQCoefficients_[i - 1]
        return val

    def getAtomDistribution(self):
        return self.atomDistribution_

    def getTheta(self):
        return self.theta_

    def getLog2Cache(self):
        return self.log2Cache_

    def getM(self):
        return self.m_

    def getRealization(self):
        realization = 0.0
        # Number of terms
        N = int(self.poisson_.getRealization()[0])
        # Sum the atoms
        for j in xrange(N):
            realization += self.atomDistribution_.getRealization()[0]
        return NumericalPoint(1, realization)

    def getNumericalSample(self, size):
        sample = NumericalSample(size, 1)
        for i in xrange(size):
            sample[i] = self.getRealization()
        return sample

    def computePDF(self, x):
        try:
            val = x[0]
        except:
            val = x
        k = int(round(val))
        # Argument not integer
        if k != val:
            return 0.0
        # Negative argument
        if k < 0:
            return 0.0
        # If the value is already in the cache, return it
        cacheSize = self.pdfCache_.getSize()
        if k < cacheSize:
            return self.pdfCache_[k]
        # If we arrive here, it is because i >= m so increase m and
        # update the caches
        while (self.m_ <= k):
            self.m_ = 2 * self.m_
        self.fillComputationCache()
        return self.pdfCache_[k]

    def computeCDF(self, x, tail = False):
        try:
            val = x[0]
        except:
            val = x
        k = int(round(val))
        if k < 0.0:
            if tail:
                return 1.0
            else:
                return 0.0
        # If the value is already in the cache, return it
        cacheSize = self.cdfCache_.getSize()
        if k < cacheSize:
            if tail:
                return 1.0 - self.cdfCache_[k]
            else:
                return self.cdfCache_[k]
        # Compute all the values from the last stored in the cache to the needed one
        if cacheSize == 0:
            lastCDF = 0.0
        else:
            lastCDF = self.cdfCache_[cacheSize - 1]
        for i in xrange(cacheSize, k + 1):
            lastCDF += self.computePDF(i)
            if lastCDF > 1.0:
                lastCDF = 1.0
            self.cdfCache_.add(lastCDF)
        if tail:
            return 1.0 - self.cdfCache_[k]
        else:
            return self.cdfCache_[k]


    def __str__(self):
        if self.size_ == 0:
            return ""
        res = "(theta = " + str(self.lambdas_) + ", atom = " + str(self.atomDistribution_) + ")"
        return res

    def computeQuantile(self, q, tail=False):
        if (q < 0.0) or (q > 1.0):
            raise Exception('In IntegralCompoundPoisson', 'q must be in [0, 1]')
        k = 0
        if tail:
            while self.computeCDF(k, True) > q:
                k += 1
        else:
            while self.computeCDF(k) < q:
                k += 1
        return NumericalPoint(1, k)

    def getMean(self):
        return NumericalPoint(1, self.q_.derivative(1.0) * exp(self.q_(1.0)).real)

    def getCovariance(self):
        q1 = self.q_(1.0)
        qp = self.q_.derivate()
        qp1 = qp(1.0)
        qs1 = qp.derivative(1.0)
        expQ1 = exp(q1).real
        covariance = CovarianceMatrix(1)
        covariance[0, 0] = (qs1 + qp1 * (1.0 + qp1 * (1 - expQ1))) * expQ1
        return covariance

    def getStandardDeviation(self):
        return NumericalPoint(1, sqrt(self.getCovariance()[0, 0]))

    def drawPDF(self, xMin, xMax):
        support = NumericalSample(0, 1)
        weights = NumericalPoint(0)
        for i in xrange(int(ceil(xMin)), int(floor(xMax)) + 1):
            support.add(NumericalPoint(1, i))
            weights.add(self.computePDF(i))
        title = "IntegralCompoundPoisson PDF"
        graph = Graph(title, "k", "pdf", True, "topright")
        point = NumericalPoint(2)
        point[0] = xMin;
        data = NumericalSample(0, 2)
        data.add(point);
        for i in xrange(support.getSize()):
            point[0] = support[i][0]
            data.add(point)
            point[1] = self.computePDF(point[0])
            data.add(point)
            point[1] = 0.0
            data.add(point)
        point[0] = xMax
        point[1] = 0.0
        data.add(point)
        graph.addDrawable(Curve(data, "red", "solid", 2, title))
        return graph

    def drawCDF(self, xMin, xMax):
        support = NumericalSample(0, 1)
        weights = NumericalPoint(0)
        for i in xrange(int(ceil(xMin)), int(floor(xMax)) + 1):
            support.add(NumericalPoint(1, i))
            weights.add(self.computePDF(i))
        size = support.getSize()
        title = "IntegralCompoundPoisson CDF"
        graph = Graph(title, "k", "pdf", True, "topleft")
        lastX = xMin
        data = NumericalSample(size + 2, 2)
        data[0][0] = xMin
        data[0][1] = self.computeCDF(xMin)
        for i in xrange(size):
            x = support[i][0]
            data[i + 1][0] = x
            data[i + 1][1] = self.computeCDF(x)
        data[size + 1][0] = xMax
        data[size + 1][1] = self.computeCDF(xMax)
        s = Staircase(data, "red", "solid", "s")
        s.setLineWidth(2)
        s.setLegendName(title)
        graph.addDrawable(s)
        return graph
