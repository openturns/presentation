# -*- coding: utf-8 -*-
"""
To install the environment:

conda install otmorris otwrapy
"""


import openturns as ot
import time
import openturns.viewer as otv
import otwrapy as otw
import otmorris


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


isFast = False  # Set to True to make it fast

# Define model
print("+ Create Morris function")
ot.RandomGenerator.SetSeed(1)
b0 = ot.DistFunc.rNormal()
alpha = ot.DistFunc.rNormal(10)
beta = ot.DistFunc.rNormal(6 * 14)
gamma = ot.DistFunc.rNormal(20 * 14)

morris_python = ot.Function(otmorris.MorrisFunction(alpha, beta, gamma, b0))

dim = morris_python.getInputDimension()

# Define the input distribution
distributionList = [ot.Uniform(0, 1)] * 20
myDistribution = ot.ComposedDistribution(distributionList)

print("+ Create training design")
N_train = 200  # size of the experimental design

t1 = time.time()
inputTrain = myDistribution.getSample(N_train)
outputTrain = morris_python(inputTrain)
t2 = time.time()
elapsed = t2 - t1
print("Elapsed = %.2f (s)" % (elapsed))

# Create the input random vector
inputRandomVector = ot.RandomVector(myDistribution)

########################################################
#
# Part 1: Python version
#

print("Python")
(sampleSizeList_pyfun, timeList_pyfun, performanceList_pyfun) = benchGetSample(
    morris_python,
    inputRandomVector,
    minimum_size_sample=10,
    number_of_points_per_second_factor=1.0,
)

########################################################
#
# Part 2: Parallelizer version
#

print("Parallelizer")


def getParallelPerformance(backend, n_cpus):
    morris_parallel = otw.Parallelizer(morris_python, backend=backend, n_cpus=n_cpus)

    (sampleSizeList_para, timeList_para, performanceList_para) = benchGetSample(
        morris_parallel,
        inputRandomVector,
        minimum_size_sample=10,
        number_of_points_per_second_factor=1.0,
    )
    return sampleSizeList_para, timeList_para, performanceList_para


n_cpus = 4
list_of_backend = ["ipyparallel", "joblib", "pathos", "multiprocessing"]
backend = "joblib"
print("backend = ", backend)

list_of_cpus_values = [2, 4, 6, 8]
list_of_results = []
for n_cpus in list_of_cpus_values:
    parallel_result = getParallelPerformance(backend, n_cpus)
    list_of_results.append(parallel_result)

########################################################
#
# Part 4 : Make a plot
#

pointStyleList = list(ot.Drawable.GetValidPointStyles())
pointStyleList.remove("circle")
pointStyleList.remove("diamond")
pointStyleList.remove("bullet")
pointStyleList.remove("dot")
pointStyleList.remove("none")
lineStyleList = ot.Drawable.GetValidLineStyles()
palette = ot.Drawable.BuildDefaultPalette(1 + len(list_of_cpus_values))
graph = ot.Graph("Performance of Morris", "Sample size", "Points / s", True)
curveCloud = makeCurveCloud(
    sampleSizeList_pyfun,
    performanceList_pyfun,
    palette[0],
    "Python",
    pointStyleList[0],
    lineStyleList[1],
)
graph.add(curveCloud)
index = 0
for parallel_result in list_of_results:
    n_cpus = list_of_cpus_values[index]
    sampleSizeList_para, timeList_para, performanceList_para = parallel_result
    curveCloud = makeCurveCloud(
        sampleSizeList_para,
        performanceList_para,
        palette[1 + index],
        "%s (CPU = %d)" % (backend, n_cpus),
        pointStyleList[1 + index],
        lineStyleList[2 + index],
    )
    graph.add(curveCloud)
    index += 1
graph.setLogScale(ot.GraphImplementation.LOGX)
graph.setLegendPosition("topright")
view = otv.View(
    graph,
    figure_kw={"figsize": (4.0, 3.0)},
    legend_kw={"bbox_to_anchor": (1.0, 1.0), "loc": "upper left"},
)
view.getFigure().savefig("../images/benchmark_Morris_otwrapy.png", bbox_inches="tight")
