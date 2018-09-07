from openturns import *
from IntegralUserDefined import *

class IntegralUserDefinedFactory(DistributionImplementationFactory):
    def __init__(self):
        DistributionImplementationFactory.__init__(self)

    def buildImplementation(self, sample):
        dictionary = {}
        sampleSize = sample.getSize()
        for i in xrange(sampleSize):
            x = sample[i][0]
            # Negative value
            if x < 0.0:
                raise Exception('In IntegralUserDefinedFactory', 'The realizations must be nonnegative')
            k = int(round(x))
            # Not an integer
            if k != x:
                raise Exception('In IntegralUserDefinedFactory', 'The realizations must take only integral values')
            if dictionary.has_key(k):
                dictionary[k] += 1
            else:
                dictionary[k] = 0
        listItems = dictionary.items()
        print listItems
        itemSize = len(listItems)
        support = UnsignedLongCollection(itemSize)
        weights = NumericalPoint(itemSize)
        for i in xrange(itemSize):
            support[i] = listItems[i][0]
            weights[i] = listItems[i][1] / float(sampleSize)
        print "support=", support
        print "weights=", weights
        return IntegralUserDefined(support, weights)
