from openturns import *
from openturns.viewer import ViewImage
from IntegralCompoundPoisson import *
from IntegralUserDefinedFactory import *
from math import *

drawFlag = False

# First, build the atom distribution
d = IntegralUserDefined([1, 2, 4, 7], [0.1, 0.2, 0.3, 0.4])
# Second, build Poisson's theta
theta = 20.0
# Build the CompoundPoisson distribution
ICP = IntegralCompoundPoisson(d, theta)
ICPSample = ICP.getNumericalSample(100000)
userDefined = IntegralUserDefinedFactory().buildImplementation(ICPSample)
for i in xrange(1, 181):
    udPDF = userDefined.computePDF(i)
    icpPDF = ICP.computePDF(i)
    udCDF = userDefined.computeCDF(i)
    icpCDF = ICP.computeCDF(i)
    udCDFc = userDefined.computeCDF(i, True)
    icpCDFc = ICP.computeCDF(i, True)
    print "error rel % (PDF, CDF, CDF c)="
    print NumericalPoint([udPDF / icpPDF - 1.0, udCDF / icpCDF - 1.0, udCDFc / icpCDFc - 1.0]) * 100
    print "error abs (PDF, CDF, CDF c)="
    print NumericalPoint([fabs(udPDF - icpPDF), fabs(udCDF - icpCDF), fabs(udCDFc - icpCDFc)])
    
if drawFlag:
    xMin = -10.0
    xMax = 200.0
    g = ICP.drawPDF(xMin, xMax)
    drawable = userDefined.drawPDF(xMin, xMax, 10 * int(xMax - xMin + 1)).getDrawable(0)
    drawable.setColor("blue")
    drawable.setLineStyle("dotted")
    g.addDrawable(drawable)
    g.draw("ICPPDF", 1280, 1024, 1)
    ViewImage(g.getBitmap())
    g = ICP.drawCDF(xMin, xMax)
    drawable = userDefined.drawCDF(xMin, xMax, 10 * int(xMax - xMin + 1)).getDrawable(0)
    drawable.setColor("blue")
    drawable.setLineStyle("dotted")
    g.addDrawable(drawable)
    g.draw("ICPCDF", 1280, 1024, 1)
    ViewImage(g.getBitmap())
