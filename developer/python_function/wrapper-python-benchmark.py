# -*- coding: utf-8 -*-
#  Copyright (C) 2013 - 2023 - Michael Baudin - EDF R&D

"""

For OT v1.19
The simplest central tendency study.
* 3 inputs, Normal(0,1)
* 2 outputs
* Estimate Empirical Mean, Empirical Standard Deviation


**Questions**

* Exécuter le benchmark sur la machine et reproduire la figure.
* Ouvrir votre gestionnaire de processus et observer l'activité des processeurs de votre machine durant l'exécution du benchmark.

"""

import openturns as ot
import time
import numpy as np
import openturns.viewer as otv


def benchGetSample(myWrapper, inputRandomVector, max_time=4.0, sample_size_factor = 2.0):
    """
    performanceListorms a benchmark of the getSample() method.

    At each iteration, the sample size increases, which increases the 
    elapsed time. 
    The algorithm increases the sample size until the elapsed time gets greater than 
    the maximum time. 

    Parameters
    ----------
    myWrapper : ot.Function
        A function.
    inputRandomVector : ot.RandomVector()
        The input random vector.
    max_time : float, optional
        The maximum number of seconds to wait before stopping the 
        algorithm. The default is 4.0.
    sample_size_factor : float, > 1.0
        The factor which multiplies the sample size at each iteration. 

    Returns
    -------
    sampleSizeList : np.array(niter)
        The size of Monte Carlo samples.
    timeList : np.array(niter)
        The elapsed time (s).
    performanceList : np.array(niter)
        The number of Million Monte Carlo samples divided by the elapsed time (s).

    """
    # Create the output variable of interest
    outputVariableOfInterest = ot.CompositeRandomVector(myWrapper, inputRandomVector)
    #
    sampleSizeList = list()
    timeList = list()
    performanceList = list()
    size_sample = 2
    for i in range(30):
        size_sample = int(sample_size_factor * size_sample)
        start_time = time.time()
        _ = outputVariableOfInterest.getSample(size_sample)
        end_time = time.time()
        time_sample = end_time - start_time
        if time_sample == 0.0:
            # Performance is too small, skip sample size - Reset
            sampleSizeList = list()
            timeList = list()
            performanceList = list()
            continue
        performanceList_sample = size_sample / time_sample / 1.0e6
        print(
            "N=%d, Elapsed time: %.1f (s), performanceList: %.3f"
            % (size_sample, time_sample, performanceList_sample)
        )
        # Store the data
        sampleSizeList.append(size_sample)
        timeList.append(time_sample)
        performanceList.append(performanceList_sample)
        if time_sample > max_time:
            break
    return (sampleSizeList, timeList, performanceList)


########################################################
#
# Part 0 : Create the inputRandomVector

# Create the marginal distributions
distributionX0 = ot.Normal(0.0, 1.0)
distributionX1 = ot.Normal(0.0, 1.0)
distributionX2 = ot.Normal(0.0, 1.0)

# Create the input probability distribution
inputDistribution = ot.ComposedDistribution(
    (distributionX0, distributionX1, distributionX2)
)

# Create the input random vector
inputRandomVector = ot.RandomVector(inputDistribution)

########################################################
#
# Part 1 : Basic PythonFunction wrapper


def mySimulator(x):
    y0 = x[0] + x[1] + x[2]
    y1 = x[0] - x[1] * x[2]
    y = [y0, y1]
    return y


myWrapper = ot.PythonFunction(3, 2, mySimulator)

print("PythonFunction:Basic")
(sampleSizeList_pyfun, timeList_pyfun, performanceList_pyfun) = benchGetSample(
    myWrapper, inputRandomVector
)

########################################################
#
# Part 2 : Vectorized (Numpy) PythonFunction wrapper
# with func_sample option.


def mySimulatorNumpy(x):
    x = np.array(x)
    x0 = x[:, 0]
    x1 = x[:, 1]
    x2 = x[:, 2]
    y0 = x0 + x1 + x2
    y1 = x0 - x1 * x2
    y = np.vstack((y0, y1))
    y = y.transpose()
    return y


myWrapperNumpy = ot.PythonFunction(3, 2, func_sample=mySimulatorNumpy)

print("PythonFunction:func_sample (Numpy)")
(sampleSizeList_func_sample, timeList_func_sample, performanceList_func_sample) = benchGetSample(
    myWrapperNumpy, inputRandomVector
)
########################################################
#
# Part 3 : Symbolic function

myFunctionSymbolic = ot.SymbolicFunction(("x0", "x1", "x2"), ("x0 + x1 + x2", "x0 - x1 * x2"))

print("Symbolic:")
(sampleSizeList_symbolic, timeList_symbolic, performanceList_symbolic) = benchGetSample(
    myFunctionSymbolic, inputRandomVector
)
########################################################
#
# Part 4 : Make a plot
#

def makeCurveCloud(dataX, dataY, color, legend, pointStyle, lineStyle):
    """
    Create a curve-cloud graph.

    Parameters
    ----------
    dataX : ot.Sample(size, 1)
        The X data.
    dataY : ot.Sample(size, 1)
        The Y data.
    color : str
        The color.
    legend : str
        The legend.
    pointStyle : str
        The point style.
    lineStyle : str
        The line style.

    Returns
    -------
    graph : ot.Graph
        The graph.

    """
    graph = ot.Graph()
    cloud = ot.Cloud(dataX, dataY)
    cloud.setPointStyle(pointStyle)
    cloud.setLegend(legend)
    cloud.setColor(color)
    graph.add(cloud)
    curve = ot.Curve(dataX, dataY)
    curve.setLineStyle(lineStyle)
    curve.setLegend("")
    curve.setColor(color)
    graph.add(curve)
    return graph

pointStyleList = ot.Drawable.GetValidPointStyles()
lineStyleList = ot.Drawable.GetValidLineStyles()
palette = ot.Drawable.BuildDefaultPalette(3)
graph = ot.Graph("Performance of functions", "Sample size", "Million points / s", True)
curveCloud = makeCurveCloud(sampleSizeList_pyfun, performanceList_pyfun, palette[0], "Python", 
                            pointStyleList[0], "dashed")
graph.add(curveCloud)
curveCloud = makeCurveCloud(sampleSizeList_func_sample, performanceList_func_sample, palette[1], "func_sample", 
                            pointStyleList[1], "dashed")
graph.add(curveCloud)
curveCloud = makeCurveCloud(sampleSizeList_symbolic, performanceList_symbolic, palette[2], "Symbolic", 
                            pointStyleList[2], "dashed")
graph.add(curveCloud)
graph.setLogScale(ot.GraphImplementation.LOGX)
graph.setLegendPosition("topright")
view = otv.View(graph, figure_kw={"figsize": (4.0, 3.0)}, 
         legend_kw={"bbox_to_anchor":(1.0, 1.0), "loc":"upper left"})
view.getFigure().savefig("images/wrapper-python-benchmark.pdf", bbox_inches = "tight")
view.getFigure().savefig("images/wrapper-python-benchmark.png", bbox_inches = "tight")

