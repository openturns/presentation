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


def benchGetSample(
    myWrapper,
    inputRandomVector,
    max_time=4.0,
    sample_size_factor=2.0,
    minimum_size_sample=2,
    number_of_points_per_second_factor=1.0e6,
    maximum_number_of_iterations=30,
):
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
    minimum_size_sample : int, default = 2
        The minimum sample size.
    number_of_points_per_second_factor : float, > 1.0, default = 1.e6
        The factor which is used to measure the performance.
        The default is 1.0e6, which measures number of million
        points per seconds.
    maximum_number_of_iterations : int, default = 30
        The maximum number of iterations.

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
    size_sample = minimum_size_sample
    for i in range(maximum_number_of_iterations):
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
        performanceList_sample = (
            size_sample / time_sample / number_of_points_per_second_factor
        )
        print(
            "N=%d, Elapsed time: %.1f (s), performance: %.3f"
            % (size_sample, time_sample, performanceList_sample)
        )
        # Store the data
        sampleSizeList.append(size_sample)
        timeList.append(time_sample)
        performanceList.append(performanceList_sample)
        if time_sample > max_time:
            break
    return (sampleSizeList, timeList, performanceList)


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


print("PythonFunction:")
myWrapper = ot.PythonFunction(3, 2, mySimulator)
sampleSizeList_pyfun, timeList_pyfun, performanceList_pyfun = benchGetSample(
    myWrapper, inputRandomVector
)

# Parallel (this is slow in my case)
usePythonParallel = False  # Enable this to test
if usePythonParallel:
    n_cpus = -1  # Use them all
    print("PythonFunction with n_cpus = ", n_cpus)
    myWrapper = ot.PythonFunction(3, 2, mySimulator, n_cpus = -1)
    sampleSizeList_pyfun_parallel, timeList_pyfun_parallel, performanceList_pyfun_parallel = benchGetSample(
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
(
    sampleSizeList_func_sample,
    timeList_func_sample,
    performanceList_func_sample,
) = benchGetSample(myWrapperNumpy, inputRandomVector)

########################################################
#
# Part 3 : Symbolic function

isMuParserAvailable = True
if isMuParserAvailable:
    ot.ResourceMap.Set("SymbolicParser-Backend", "MuParser")
    myFunctionSymbolic = ot.SymbolicFunction(
        ("x0", "x1", "x2"), ("x0 + x1 + x2", "x0 - x1 * x2")
    )

    print("Symbolic: MuParser")
    (
        sampleSizeList_symbolic_muparser,
        timeList_symbolic_muparser,
        performanceList_symbolic_muparser,
    ) = benchGetSample(myFunctionSymbolic, inputRandomVector)

ot.ResourceMap.Set("SymbolicParser-Backend", "ExprTk")
myFunctionSymbolic = ot.SymbolicFunction(
    ("x0", "x1", "x2"), ("x0 + x1 + x2", "x0 - x1 * x2")
)

print("Symbolic: ExprTk")
(
    sampleSizeList_symbolic_exprtk,
    timeList_symbolic_exprtk,
    performanceList_symbolic_exprtk,
) = benchGetSample(myFunctionSymbolic, inputRandomVector)

########################################################
#
# Part 4 : Make a plot
#



pointStyleList = ot.Drawable.GetValidPointStyles()
lineStyleList = ot.Drawable.GetValidLineStyles()
palette = ot.Drawable.BuildDefaultPalette(5)
graph = ot.Graph("Performance of functions", "Sample size", "Million points / s", True)
curveCloud = makeCurveCloud(
    sampleSizeList_pyfun,
    performanceList_pyfun,
    palette[0],
    "Python",
    "circle",
    "dashed",
)
graph.add(curveCloud)
curveCloud = makeCurveCloud(
    sampleSizeList_func_sample,
    performanceList_func_sample,
    palette[1],
    "func_sample",
    "diamond",
    "dashed",
)
graph.add(curveCloud)
if usePythonParallel:
    curveCloud = makeCurveCloud(
        sampleSizeList_pyfun_parallel,
        performanceList_pyfun_parallel,
        palette[2],
        "func and //",
        "triangledown",
        "dashed",
    )
    graph.add(curveCloud)
# Symbolic : MuParser
if isMuParserAvailable:
    curveCloud = makeCurveCloud(
        sampleSizeList_symbolic_muparser,
        performanceList_symbolic_muparser,
        palette[3],
        "Symbolic(MuParser)",
        "fsquare",
        "dashed",
    )
    graph.add(curveCloud)
# Symbolic : ExprTk
curveCloud = makeCurveCloud(
    sampleSizeList_symbolic_exprtk,
    performanceList_symbolic_exprtk,
    palette[4],
    "Symbolic(ExprTk)",
    "ftriangleup",
    "dashed",
)
graph.add(curveCloud)
#
graph.setLogScale(ot.GraphImplementation.LOGX)
graph.setLegendPosition("topright")
view = otv.View(
    graph,
    figure_kw={"figsize": (4.0, 3.0)},
    legend_kw={"bbox_to_anchor": (1.0, 1.0), "loc": "upper left"},
)
# view.getFigure().savefig("../images/wrapper-python-benchmark.pdf", bbox_inches = "tight")
view.getFigure().savefig("../images/wrapper-python-benchmark.png", bbox_inches="tight")
