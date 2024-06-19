# -*- coding: utf-8 -*-
"""
### Exercice 5 : configurer le nombre de cpus
L'option `n_cpus` de la classe `PythonFunction` permet de configurer le nombre de processeurs. L'implémentation est fondée sur le module `multiprocessing`. Dans cet exercice, on cherche à observer l'effet de cette option sur la performance du calcul.

Pour observer un changement dans la performance nous nous plaçons dans la situation suivante :
- la fonction possède un grand nombre de variables d'entrées,
- la fonction est coûteuse.

Dans ce but, nous définissons la fonction suivante.
"""
import openturns as ot
import multiprocessing
import math
import time


def myHighDimSimulator(x):
    dim = ot.Point(x).getDimension()
    y0 = 0.0
    y1 = 1.0
    for i in range(dim):
        y0 = y0 + math.exp(x[i])
        y1 = y1 * math.exp(x[i])
    y = [y0, y1]
    return y


dim = 5
inputHighDimDistribution = ot.ComposedDistribution([ot.Normal()] * dim)
inputHighDimRandomVector = ot.RandomVector(inputHighDimDistribution)

"""
**Questions**

- Utiliser le module `time` pour mesurer la performance de la fonction sans l'option n_cpus. Pour observer une durée de simulation significative, augmentez la taille du plan d'expériences ou le nombre de dimensions.
- De même avec l'option `n_cpus`.
- Quelle différence constatez-vous ?
"""
"""
### Solution de l'exercice 5
"""


def benchMyPythonFunction(inputRandomVector, mypyfunction, sampleSize, label):
    t0 = time.time()
    outputVect = ot.CompositeRandomVector(mypyfunction, inputRandomVector)
    _ = outputVect.getSample(sampleSize)
    t1 = time.time()
    print("Elapsed = %.2f (s)" % (t1 - t0))
    return


sampleSize = 1000

print("+ Default Python function")
myPyFunction1 = ot.PythonFunction(dim, 2, myHighDimSimulator)
benchMyPythonFunction(
    inputHighDimRandomVector, myPyFunction1, sampleSize, "Without n_cpus"
)

n_cpus = multiprocessing.cpu_count()
print("n_cpus = ", n_cpus)

print("+ With n_cpus")
myPyFunction2 = ot.PythonFunction(dim, 2, myHighDimSimulator, n_cpus=n_cpus)
benchMyPythonFunction(
    inputHighDimRandomVector, myPyFunction2, sampleSize, "With n_cpus"
)
