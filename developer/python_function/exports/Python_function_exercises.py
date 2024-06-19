#!/usr/bin/env python
# coding: utf-8

# # Python functions
#
# **Coding party OpenTURNS, march 2023**
#
# Michaël Baudin
#
# Mathieu Couplet
#

# ## Résumé
#
# Dans cette page, nous présentons comment connecter OpenTURNS à un code de calcul. C'est en effet une étape indispensable pour pouvoir, par exemple, propager les incertitudes au travers de cette fonction.
#
# Objectifs de cette page :
# * Introduction
# * PythonFunction
# * PythonFunction vectorisée
# * PythonFunction avec historique
# * Comparer les techniques en termes de performance

# ## Références
#
# * User Manual, Functions [Lien](http://openturns.github.io/openturns/master/user_manual/functions.html)
# * Examples, Functional modeling : [Lien](http://openturns.github.io/openturns/master/examples/functional_modeling/functional_modeling.html)
#
# * Classe MemoizeFunction : [Lien](http://openturns.github.io/openturns/master/user_manual/_generated/openturns.MemoizeFunction.html)
#
# * Sur ExprTk : OpenTURNS Users’ Day #11, Friday, the 15 th, June 2018, Denis Barbier, [Lien](http://trac.openturns.org/blog/OpenTURNS_Users_Day_11)

# ## Utilisation d’une fonction
#
# L'utilisation typique consiste à :
# * créer une `Function`,
# * l’utiliser pour créer un `RandomVector`.
#
# Exemple :
#
# ```
# [...]
# myWrapper = PythonFunction ( MyWrapperClass ())
# [...]
# outVariable = CompositeRandomVector ( myWrapper , inRandomVector )
# [...]
# ```
#

# Autres exemples d’utilisation :
#
# * Calibration bayésienne : voir `RandomWalkMetropolisHastings`
# * Processus stochastiques : voir `SpatialFunction` et `TemporalFunction`
# * Optimisation : voir OptimizationProblem
# * Fonctions paramétriques : voir méthodes `setParameters` et `getParameters` (version > 1.7).

# ## Exemple fil rouge
#
# Pour chaque wrapper, nous illustrons la connexion avec l’exemple suivant :
# * 3 entrées, de loi normale standard, indépendantes
# * 2 sorties
# * Formule analytique
# * Echange de données par fichiers XML.
#
# La formule analytique est donnée par :
# $$
# \begin{eqnarray}
# Y_1 &=& X_1 + X_2 + X_3 \\
# Y_2 &=& X_1 − X_2 X_3
# \end{eqnarray}
# $$
#
# Les résultats exacts sont les suivants.
#
# | Variable | Espérance | Ecart-type |
# |-|-|-|
# | $Y_1$ | 0 | 1.732 |
# | $Y_2$ | 0 | 1.415 |
#

# In[1]:


import openturns as ot
import numpy as np
import time
import math
import multiprocessing

ot.__version__


# In[2]:


X0 = ot.Normal(0.0, 1.0)
X1 = ot.Normal(0.0, 1.0)
X2 = ot.Normal(0.0, 1.0)
inputDistribution = ot.ComposedDistribution((X0, X1, X2))
inputRandomVector = ot.RandomVector(inputDistribution)


# ## PythonFunction : constructeur
#
# La classe `PythonFunction` permet de créer une fonction OpenTURNS en utilisant une fonction Python créée avec l'opérateur `def`.
#
# <img src="images/wrapper_OT-PythonFunction.svg" width="400px">
#
# Le constructeur de la classe PythonFunction est
#
# `PythonFunction ( nbInputs , nbOutputs , myPythonFunc )`
#
# où
# * `nbInputs` : nombre de variables d’entrées,
# * `nbOutputs` : nombre de variables de sorties,
# * `myPythonFunc` : une fonction Python.

# Le simulateur `mySimulator` a la séquence d'appel `y=mySimulator(x)` où
# * `x` : l’entrée du simulateur, un vecteur de taille `nbInputs`,
# * `y` : la sortie du simulateur, un vecteur de taille `nbOutputs`.

# In[3]:


def mySimulator(x):
    y0 = x[0] + x[1] + x[2]
    y1 = x[0] - x[1] * x[2]
    y = [y0, y1]
    return y


# ## Exemple d'utilisation de la PythonFunction
#
# Dans l'exemple suivant, on estime la moyenne par Monte-Carlo simple sur la base de 10000 expériences.

# In[4]:


myWrapper = ot.PythonFunction(3, 2, mySimulator)
outputVect = ot.CompositeRandomVector(myWrapper, inputRandomVector)
montecarlosize = 10000
outputSample = outputVect.getSample(montecarlosize)
empiricalMean = outputSample.computeMean()
print(empiricalMean)
empiricalSd = outputSample.computeStandardDeviation()
print(empiricalSd)


# ## Quel type pour x, pour y ?
#
# | Type | Entrée X | Sortie Y |
# |-|-|-|
# | list (Python) | | ✓ |
# | tuple (Python) | | ✓ |
# | array (NumPy) | | ✓ |
# | Point (OpenTURNS) | ✓ | ✓ |
#

# ## PythonFunction : Objectifs, Avantages, Inconvénients
#
# Les objectifs de la classe `PythonFunction` sont :
# * Simplicité de mise en oeuvre.
# * Directement en Python : possibilité d’utiliser tous les modules Python pour réaliser le calcul, ou la connexion.
#
# Avantages :
# * Utile si le simulateur est disponible en Python.
# * Peut se combiner avec les "Coupling Tools".
# * Possibilité de vectorisation avec l’option `func_sample`.
# * Peut être parallélisé sur plusieurs processeurs avec l'option n_cpus (voir l'exercice 5).
#
# Inconvénients :
# * Pas de calcul exact des dérivées.

# ## PythonFunction vectorisée : Objectifs, Avantages, Inconvénients
#
# La classe PythonFunction possède une option `func_sample` :
# * Idée : améliorer la performance en vectorisant les opérations.
# * Principe : évaluer toutes les sorties en fonction de toutes les entrées en un seul appel à la fonction, sans boucle `for`.
# * Implémentation : l’entrée et la sortie sont des `Sample` (et non plus des vecteurs).
#
# Avantages :
# * Amélioration de la performance.
#
# Inconvénients :
# * Nécessite de vectoriser le calcul.

# ## Prototype
#
# ```
# def mySimulator (x):
#     [...]
#     return y
# myWrapper=PythonFunction(nbInputs, nbOutputs, func_sample=mySimulator)
# ```
#
# où
# * x : l’entrée du simulateur, un `NumericalSample` de taille `nbExperiments` (`getSize`), de dimension `nbInputs` (`getDimension`),
# * y : la sortie du simulateur
#   * un `array` : `nbExperiments` lignes et `nbOutputs` colonnes
#   * un `NumericalSample` : taille `nbExperiments` et dimension `nbOutputs`

# ## PythonFunction vectorisée : exemple avec Numpy
#

# In[5]:


def mySimulatorVect(x):
    # Conversion NumericalSample > Array Numpy
    x = np.array(x)
    x0 = x[:, 0]  # Extraction de la colonne 0
    x1 = x[:, 1]
    x2 = x[:, 2]
    y0 = x0 + x1 + x2
    y1 = x0 - x1 * x2
    # Empilement de deux lignes
    y = np.vstack((y0, y1))
    y = y.transpose()
    return y


myWrapperVect = ot.PythonFunction(3, 2, func_sample=mySimulatorVect)


# In[6]:


outputVect = ot.CompositeRandomVector(myWrapperVect, inputRandomVector)
montecarlosize = 10000
outputSample = outputVect.getSample(montecarlosize)

empiricalMean = outputSample.computeMean()
print(empiricalMean)
empiricalSd = outputSample.computeStandardDeviation()
print(empiricalSd)


# ## MemoizeFunction pour gérer l'historique
#
# La classe `MemoizeFunction` définit un mécanisme d’historique des appels à G.
#
# | Méthodes | Fonction |
# |-|-|
# | `enableHistory()` | active l’historique (défaut : activé) | |
# | `disableHistory()` | désactive l’historique |
# | `isHistoryEnabled()` | vrai si l’historique est actif |
# | `clearHistory()` | vide l’historique |
# | `getHistoryInput()` | un `NumericalSample`, historique des entrées X |
# | `getHistoryOutput()` | un `NumericalSample`, historique des sorties Y |

# In[7]:


myWrapper = ot.PythonFunction(3, 2, mySimulator)
myWrapper = ot.MemoizeFunction(myWrapper)


# In[8]:


outputVariableOfInterest = ot.CompositeRandomVector(myWrapper, inputRandomVector)
montecarlosize = 10
outputSample = outputVariableOfInterest.getSample(montecarlosize)


# Récupère l'historique en entrée.

# In[9]:


inputs = myWrapper.getInputHistory()
inputs


# Récupère l'historique en sortie

# In[10]:


outputs = myWrapper.getOutputHistory()
outputs


# ##  Exercices
#
#
# ### Exercice 1 : une fonction avec 4 entrées
#
# Exemple : WrapperPython/studyCenterSimple.py
#
# On considère un nouveau modèle, avec une nouvelle variable de sortie
# Y3 et une nouvelle variable d’entrée X4 :
# $$
# \begin{eqnarray}
# Y_1 &=& X_1 + X_2 + X_3 \\
# Y_2 &=& X_1 − X_2 X_3 \\
# Y_3 &=& 2 X_1 + 3 X_2 + 4 X_4
# \end{eqnarray}
# $$
#
# **Questions**
#
# * Modifier la fonction Python pour simuler le nouveau modèle.
# * Ajouter une nouvelle variable X4 de loi normale standard dans le modèle probabiliste.
# * Estimer la moyenne de la sortie par Monte-Carlo simple.
#

# ### Solution de l'exercice 1 : une fonction avec 4 entrées
#

# In[11]:


def mySimulator(x):
    y0 = x[0] + x[1] + x[2]
    y1 = x[0] - x[1] * x[2]
    y2 = 2 * x[0] + 3 * x[1] + 4 * x[3]
    y = [y0, y1, y2]
    return y


myWrapper = ot.PythonFunction(4, 3, mySimulator)
# Create the marginal distributions
X0 = ot.Normal(0.0, 1.0)
X1 = ot.Normal(0.0, 1.0)
X2 = ot.Normal(0.0, 1.0)
X3 = ot.Normal(0.0, 1.0)
# Create the input probability distribution
inputDistribution = ot.ComposedDistribution((X0, X1, X2, X3))
# Create the input random vector
inputRandomVector = ot.RandomVector(inputDistribution)
# Create the output variable of interest
outputVariableOfInterest = ot.CompositeRandomVector(myWrapper, inputRandomVector)
# Probabilistic Study: central dispersion
montecarlosize = 10000
# Start the simulations
outputSample = outputVariableOfInterest.getSample(montecarlosize)
# Get the empirical mean and standard deviations
outputDim = myWrapper.getOutputDimension()
outputSample.computeMean()


# ### Exercice 2 : gradient d'une fonction Python
#
# OT peut calculer la dérivée approchée d’une fonction Python par différences finies. On peut paramétrer la formule de différence utilisée, ainsi que le pas de différenciation de cette formule. De plus, lorsque la matrice Jacobienne est implémentée dans une fonction Python, on peut transmettre cette fonction à OpenTURNS pour qu'il l'utilise.
#
# **Questions**
# * Définir la fonction `myWrapper` comme dans l’exemple précédent.
# * Utiliser la méthode `gradient` de l’objet `myWrapper` pour évaluer le
# gradient G'(x) au point d’entrée X = (1, 2, 3).
# * Utiliser la méthode `hessian` de l’objet `myWrapper` pour évaluer la
# matrice Hessienne de G.
#
# * Utiliser les instructions suivantes pour configurer un gradient calculé
# par une formule de différences finies décentrée, avec un pas h = 10−2.
#
# ```
# wrapImpl = myWrapper.getEvaluation()
# h = 1.e -2
# myGradient = ot.NonCenteredFiniteDifferenceGradient(h, wrapImpl)
# myWrapper.setGradient ( myGradient )
# ```
#
# * Evaluer à nouveau le gradient avec la méthode gradient et comparer avec le résultat précédent.
# * On peut transmettre à OT une fonction Python qui évalue le gradient. Pour cela on peut utiliser la séquence d'appel :
# ```
# myWrapper = ot.PythonFunction(nbInputs, nbOutputs, mySimulator, gradient=mySimulatorGradient)
# ```
# où `mySimulatorGradient` est une fonction Python qui évalue le gradient.
# Calculez à la main des dérivées partielles de la fonction G associée à l'exemple fil rouge.
# Puis définissez la fonction `mySimulatorGradient` qui évalue la matrice Jacobienne. Puisqu'il y a trois variables d'entrée, la liste renvoyée par mySimulatorGradient doit contenir trois éléments. Chaque élément doit contenir une sous-liste de taille 2 contenant les dérivées de chaque sortie. Enfin, construisez le wrapper associé avec l'option `gradient`.
#
#

# ### Solution de l'exercice 2 : gradient d'une fonction Python

# In[12]:


def mySimulator(x):
    y0 = x[0] + x[1] + x[2]
    y1 = x[0] - x[1] * x[2]
    y = [y0, y1]
    return y


inputDim = 3
outputDim = 2
myWrapper = ot.PythonFunction(inputDim, outputDim, mySimulator)

# Evaluer le gradient
d = myWrapper.gradient([1, 2, 3])
print("type(d)=", type(d))  # OT Matrix
print("Gradient par DF=")
print(d)

# Evaluer la hessienne
dd = myWrapper.hessian([1, 2, 3])
print("type(dd)=", type(dd))  # OT SymmetricTensor
print("Hessienne=")
print(dd)

# Configurer la formule de différences finies du gradient
wrapImpl = myWrapper.getEvaluation()
myGradient = ot.NonCenteredFiniteDifferenceGradient(1.0e-2, wrapImpl)
myWrapper.setGradient(myGradient)

d = myWrapper.gradient([1, 2, 3])
print("Gradient par DF non centrée=")
print(d)


# Configurer le gradient avec une fonction Python
def mySimulatorGradient(x):
    dyx0 = [1.0, 1.0]
    dyx1 = [1.0, -x[2]]
    dyx2 = [1.0, -x[1]]
    y = [dyx0, dyx1, dyx2]
    return y


myWrapper = ot.PythonFunction(3, 2, mySimulator, gradient=mySimulatorGradient)
d = myWrapper.gradient([1, 2, 3])
print("d - Exact =")
print(d)


# ### Exercice 3 : gestion de l'historique d'une fonction Python
#
# **Questions**
#
# * Observer le changement de la valeur de retour de `isHistoryEnabled`
# * Quelles sont les méthodes qui permettent de récupérer les historiques des entrées et des sorties ?
# * Comment avoir le nombre d’appels à la fonction ?
# * Utiliser la méthode `clearHistory` et vérifier que l'historique est vide après cet appel.

# ### Solution de l'exercice 3 : gestion de l'historique d'une fonction Python

# In[13]:


def mySimulator(x):
    y0 = x[0] + x[1] + x[2]
    y1 = x[0] - x[1] * x[2]
    y = [y0, y1]
    return y


myWrapper = ot.PythonFunction(3, 2, mySimulator)
myWrapper = ot.MemoizeFunction(myWrapper)

# Create the marginal distributions
X0 = ot.Normal(0.0, 1.0)
X1 = ot.Normal(0.0, 1.0)
X2 = ot.Normal(0.0, 1.0)

# Create the input probability distribution
inputDistribution = ot.ComposedDistribution((X0, X1, X2))
# Create the input random vector
inputRandomVector = ot.RandomVector(inputDistribution)
# Create the output variable of interest
outputVariableOfInterest = ot.CompositeRandomVector(myWrapper, inputRandomVector)
# Probabilistic Study: central dispersion
montecarlosize = 20
outputSample = outputVariableOfInterest.getSample(montecarlosize)

# Get the history
inputs = myWrapper.getInputHistory()
print("inputs")
print(inputs)
outputs = myWrapper.getOutputHistory()
print("outputs")
print(outputs)
# Nombre d'appels à la fonction G
nGEvals = inputs.getSize()
print("nGEvals = %d" % (nGEvals))

# Clear the history
myWrapper.clearHistory()

# See how the history is now empty
print("After clearHistory:")
myWrapper.getOutputHistory()


# ### Exercice 4 : benchmark
#
# Voir `wrapper-python-benchmark.py`.

# ### Exercice 5 : configurer le nombre de cpus
#
# Voir le script `test_n_cpus.py`.

# ### Exercice 6 : utiliser otwrapy
#
# **Questions**
# - Installer otwrapy.
# - Consulter la documentation [de la classe Parallelizer](https://openturns.github.io/otwrapy/master/_generated/otwrapy.Parallelizer.html#otwrapy.Parallelizer).
# - Paralléliser l'évaluation de la fonction avec l'option `n_cpus`.
# - Tester les 4 options de l'argument optionnel `backend` : ‘ipyparallel’, ‘joblib’, pathos, or ‘multiprocessing’.

# ### Exercice 7 : utiliser Jax
#
# **Questions**
# - Installer Jax.
# - Consulter la documentation [le Quickstart](https://jax.readthedocs.io/en/latest/notebooks/quickstart.html).
# - Dériver la fonction `Ishigami`.
