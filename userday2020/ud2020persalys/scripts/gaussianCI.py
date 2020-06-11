# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 09:55:53 2019

Draw a gaussian confidence interval

@author: C61372
"""

import openturns as ot

X = ot.Normal()

alpha = 0.05
confidenceInterval = X.computeBilateralConfidenceInterval(1-alpha)
lb = confidenceInterval.getLowerBound()[0]
ub = confidenceInterval.getUpperBound()[0]
print("Lower bound = %f" % (lb))
print("Upper bound = %f" % (ub))

lbPDF = X.computePDF(lb)
ubPDF = X.computePDF(ub)
lbCDF = X.computeCDF(lb)
ubCDF = X.computeCDF(ub)

import pylab as pl
from openturns.viewer import View
graph = X.drawPDF()
myfig = View(graph).getFigure()
graph.setLegends(["PDF"])
pl.plot([lb,lb],[0.,lbPDF],"b-",label="%.4f conf. int." % (1-alpha))
pl.plot([ub,ub],[0.,ubPDF],"b-")
pl.legend(loc='upper right')

import pylab as pl
from openturns.viewer import View
graph = X.drawCDF()
myfig = View(graph).getFigure()
graph.setLegends(["CDF"])
pl.plot([lb,lb],[0.,lbCDF],"b-",label="%.4f conf. int." % (1-alpha))
pl.plot([ub,ub],[0.,ubCDF],"b-")
pl.legend(loc='upper left')


bu = X.computeQuantile(1-alpha/2)[0]
bl = X.computeQuantile(alpha/2)[0]
print("Quantile at level %.4f = %.4f" % (1-alpha/2,bu))
print("Quantile at level %.4f = %.4f" % (alpha/2,bl))


