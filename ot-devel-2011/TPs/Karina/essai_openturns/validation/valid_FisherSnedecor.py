from openturns import *
from openturns.viewer import *
from time import time
d1 = 20
d2 = 30
distribution = FisherSnedecor(d1, d2)
distributionChi = ChiSquare(d1)
print "mean=", distribution.getMean()
size = 1000
t0 = time()
sample = distribution.getNumericalSample(size)
print "speed=", size / (time() - t0), "real/s"
# CDF
graphCDF = distribution.drawCDF()
drawable = UserDefined(sample).drawCDF().getDrawable(0)
drawable.setColor("blue")
graphCDF.addDrawable(drawable)
graphCDF.draw("ValidCDF")
ViewImage(graphCDF.getBitmap())
# PDF
graphPDF = distribution.drawPDF()
smoothed = KernelSmoothing().buildImplementation(sample)
drawable = smoothed.drawPDF().getDrawable(0)
drawable.setColor("blue")
graphPDF.addDrawable(drawable)
graphPDF.draw("ValidPDF")
# CDF smoothed
drawable = smoothed.drawCDF().getDrawable(0)
drawable.setColor("green")
graphCDF.addDrawable(drawable)
graphCDF.draw("ValidCDF2")
