from openturns import *

class IntegralUserDefined(UserDefined):
    def __init__(self, support, weights):
        # Convertion to an UnsignedLongCollection
        tmp = UnsignedLongCollection(len(support))
        for i in xrange(len(support)):
            tmp[i] = support[i]
        support = tmp
        # Convertion to a NumericalPoint
        tmp = NumericalPoint(len(weights))
        for i in xrange(len(weights)):
            tmp[i] = weights[i]
        weights = tmp
        # Check the compatibility between support and weights
        if (support.getSize() !=  weights.getSize()):
            raise Exception('In IntegralUserDefined', 'The support and the weights must have the same size')
        # Check the validity of the support and the weights
        self.supportSize_ = support.getSize()
        for i in xrange(self.supportSize_):
            if (support[i] != round(support[i])) or (support[i] < 0.0):
                raise Exception('In IntegralUserDefined', 'The support must contain only nonnegative integers')
            if (weights[i] < 0) or (weights[i] > 1.0):
                raise Exception('In IntegralUserDefined', 'The weights must be in [0, 1]')
        # Build the underlying UserDefined distribution
        sample = NumericalSample(self.supportSize_, 1)
        for i in xrange(self.supportSize_):
            sample[i] = NumericalPoint(1, support[i])
        self.normalizedWeights_ = weights * (1.0 / sum(weights))
        UserDefined.__init__(self, sample, self.normalizedWeights_)
        self.setName("IntegralUserDefined")
        self.support_ = support
        self.weights_ = weights

    def getSupport(self):
        return self.support_

    def getWeights(self):
        return self.weights_

    def getNormalizedWeights(self):
        return self.normalizedWeights_

    def getClassName(self):
        return "IntegralUserDefined"
    
    def __str__(self):
        if self.supportSize_ == 0:
            return ""
        res = "["
        for i in xrange(self.supportSize_):
            if i > 0:
                res += "; "
            res += "(x = " + str(self.support_[i]) + ", p = " + str(self.normalizedWeights_[i]) + ")"
        res += "]"
        return res
