# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 09:13:16 2016

@author: C61372

Estimates the central dispersion by Monte-Carlo. 
"""
from math import sqrt, log10
from time import time
from numpy import zeros
import openturns as ot

'''
Computes a confidence interval for empirical mean, 
assuming the data is normal.

Parameters
alpha : the level of the confidence interval
mu : the mean
sigma : the standard deviation
n : the number of outcomes
low : the lower bound of the confidence interval
up : the upper bound of the confidence interval

Description

Assumes that X is a normal random variable with mean mu 
and variance sigma^2.
Then the empirical mean is computed :
    
    mean=(x1+...+xn)/n
    
Then we have :

P(low < mean < up) = 1-level

To get a 95% confidence interval, we use alpha=0.05.

This functions produces an approximate C.I. 
when the mean and the variance are estimated 
from a sample of independent outcomes with given, 
but unknown, distribution. 
This approximate C.I. converges when n grows.

We use the Normal distribution to compute the 
C.I.
In theory, the Student distribtion with n-1 degrees 
of freedom should be used when the variance is unknown, 
but this makes little difference as soon as n>10.

Example
# Sheldon Ross, Example 7.3a, page 241
from numpy import mean, std
x = [5, 8.5, 12, 15, 7, 9, 7.5, 6.5, 10.5]
n = len(x)
mu = mean(x)
sigma = std(x,ddof=1) # Unbiased
alpha=.05
[ low, up ] = meanCI(mu,sigma,n)
# Then P(6.986 <= mu <= 11.013) = 0.95
# where mu=9.0

Bibliography
"Introduction to probability and statistics for 
engineers and scientists", Sheldon Ross, 
Third Edition, 2004
'''
def meanCI(mu,sigma,n,alpha=0.05):
    X=ot.Normal(0,1)
    f=X.computeQuantile(alpha/2,True)[0]
    delta = f*sigma/sqrt(n)
    low=mu-delta
    up=mu+delta
    return [low,up]

def centralDispersionPrintResults(sample,alpha):
    """
    Prints the results of a central tendency analysis
    
    Parameters
    sample : a NumericalSample, the data
    alpha : a double, in [0,0.5], the confidence level
    """
    outputdim=sample.getDimension()
    samplesize = sample.getSize()
    print("Sample size : %d" % (samplesize))
    print("Sample dimension : %d" % (outputdim))
    empiricalMean = sample.computeMean()
    empiricalSd = sample.computeStandardDeviationPerComponent()
    cov = computeMeanPerComponentCov(sample)
    for i in range(outputdim):
        print("Output #%d" % (i))
        [low,up]=meanCI(empiricalMean[i],empiricalSd[i],samplesize,alpha)
        print("\t Mean=%f in [%f,%f] at %.1f%%" % (empiricalMean[i], low, up,(1-alpha)*100))
        print("\t CV(Mean) = %.2f%%" % (100*cov[i]))
    return None

def computeMeanPerComponentCov(sample):
    """
    Computes the (absolute) componentwise coefficient of 
    variation of the mean.
    
    Parameters
    sample : a NumericalSample, the data
    """
    outputdim=sample.getDimension()
    samplesize = sample.getSize()
    empiricalMean = sample.computeMean()
    empiricalSd = sample.computeStandardDeviationPerComponent()
    cov=zeros(outputdim)
    for i in range(outputdim):
        cov[i]=empiricalSd[i]/abs(empiricalMean[i])/sqrt(samplesize)
    return cov

def computeMaxCov(sample):
    """
    Computes the (absolute) coefficient of variation for the mean, 
    as the maximum C.O.V. over the outputs.
    
    Calling Sequence
    maxcov = computeMaxCov(sample)
    
    Parameters
    sample : a NumericalSample, the data
    """
    cov = computeMeanPerComponentCov(sample)
    maxcov=max(cov)
    return maxcov

def centralDispersionByMonteCarlo(randomVector, blocksize=100,maxcov=0.01,maxcalls=10000,maxelapsetime=10):
    """
    Estimates the central dispersion by Monte-Carlo
    
    Calling Sequence
    outputSample, criteria = centralDispersionByMonteCarlo(randomVector, blocksize=100,maxcov=0.01,maxcalls=10000,maxelapsetime=10)
    
    Parameters
    randomVector : a RandomVector
    blocksize : an int, the block size
    maxcov : the maximum coefficient of variation of the sample mean
    maxcalls : the maximum number of function calls
    maxelapsetime : the maximum elapsed time
    outputSample : a NumericalSample, the sample matching the criteria
    criteria : an integer, the criteria which is met
    
    Description
    Computes an output sample for central dispersion study 
    by performing the least possible number of function 
    calls such that :
    1 : the maximum coefficient of variation of the mean is < maxcov
    2 : the maximum elapsed time is > maxelapsetime
    3 : the maximum number of function calls is > maxcalls
    
    Assumes that the block size is large enough so that 
    the sample mean has an approximately normal distribution 
    with mean equal to mu and standard deviation equal to sigma/sqrt(n), 
    where mu is the expectation of the randomVector and sigma is 
    its standard deviation. 
    """
    starttime=time()
    outputSample=randomVector.getSample(blocksize)
    elapsedtime=time() - starttime
    iteration=0
    criteria=None
    while(True):
        iteration=iteration+1
        samplesize = outputSample.getSize()
        cov=computeMaxCov(outputSample)
        print("Iter. #%d, N=%d, CV(Mean)=%.2f%%, Elapsed=%.2f (s)" % \
            (iteration,samplesize,100*cov,elapsedtime))
        # Criterias
        if (samplesize>maxcalls): # Criteria 1
            criteria=1
            break
        if (cov<maxcov): # Criteria 2
            criteria=2
            break
        if (elapsedtime>maxelapsetime): # Criteria 3
            criteria=3
            break
        # We need more accuracy, we need a larger sample
        blockSample = randomVector.getSample(blocksize)
        elapsedtime=time() - starttime
        outputSample.add(blockSample)
    return outputSample, criteria

def centralDispersionPrintParameters(blocksize, maxcov, maxcalls,maxelapsetime,alpha):
    print("Central Dispersion Parameters")
    print("Block size : %d" % (blocksize))
    print("Confidence level : %f%%" % (100*(1-alpha)))
    print("Max. Coefficient of Variation : %f" % (maxcov))
    print("Max. Elapsed time : %.2f (s)" % (maxelapsetime))
    print("Max. Number of function calls : %d" % (maxcalls))
    return None
