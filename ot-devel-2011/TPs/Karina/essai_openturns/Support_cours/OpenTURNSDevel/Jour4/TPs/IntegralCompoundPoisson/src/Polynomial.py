from openturns import *

def denseToSparse(polynomial):
    degrees = UnsignedLongCollection(0)
    coefficients = NumericalPoint(0)
    deg = polynomial.getDegree()
    coeffs = polynomial.getCoefficients()
    for i in xrange(deg):
        c = coeffs[i]
        if c != 0.0:
            degrees.add(i)
            coefficients.add(c)
    return degrees, coefficients

def buildUniVariatePolynomial(degrees, coefficients):
    d = max(degrees)
    fullCoefficients = NumericalPoint(d + 1, 0.0)
    for i in xrange(len(degrees)):
        fullCoefficients[degrees[i]] += coefficients[i]
    return UniVariatePolynomial(fullCoefficients)

def truncateUniVariatePolynomial(polynomial, truncation):
    if polynomial.getDegree() <= truncation:
        return polynomial
    coefficients = NumericalPoint(truncation + 1)
    coeffPoly = polynomial.getCoefficients()
    for i in xrange(truncation):
        coefficients[i] = coeffPoly[i]
    return UniVariatePolynomial(coefficients)
