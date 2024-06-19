#!/usr/bin/env python
# coding: utf-8

# # Wrappers - Fonctions paramétriques
#
# ## Formation OpenTURNS, septembre 2018
#
# Michaël Baudin
#
# Mathieu Couplet
#
# EDF R&D
#
# 6, quai Watier
#
# 78401 Chatou
#
# michael.baudin@edf.fr
#
# mathieu.couplet@edf.fr

# ## Résumé
#
# Dans la plupart des cas, la fonction G a des paramètres (fixes).
# * Paramètres numériques : caractéristiques mécaniques, fluides (viscosité), géométriques, thermiques, électriques, etc...
# * Paramètres entiers : choix d’une méthode numérique, choix du modèle physique, etc...
# * Chaînes de caractères : chemin vers un dossier, vers un fichier, description d’une variable, etc...
#
# Ces paramètres ne sont pas des variables aléatoires : on ne veut pas les
# faire varier.
#
# Objectifs de cette séquence :
# * La classe `ParametricFunction` (Exercice 1)
# * La classe `OpenTURNSPythonFunction` (Exercice 2)

# ## Références
#
# * Ishigami, T., & Homma, T. (1990, December). An importance quantification technique in uncertainty analysis for computer models. In Uncertainty Modeling and Analysis, 1990. Proceedings., First International Symposium on (pp. 398-403). IEEE.
# * http://openturns.github.io/openturns/master/examples/functional_modeling/parametric_function.html
# * http://openturns.github.io/openturns/master/user_manual/_generated/openturns.ParametricFunction.html
# * http://openturns.github.io/openturns/master/user_manual/_generated/openturns.Function.html
# * http://openturns.github.io/openturns/master/user_manual/_generated/openturns.OpenTURNSPythonFunction.html
#

# ## Exemple
#
# On considère la fonction test Ishigami.
#

# In[1]:


import openturns as ot
import math


def ishigamiG(x):
    a = 7.0
    b = 0.1
    y = math.sin(x[0]) + a * math.sin(x[1]) ** 2 + b * x[2] ** 4 * math.sin(x[0])
    return [y]


myWrapper = ot.PythonFunction(3, 1, ishigamiG)

p = math.pi / 2
X = [p, p, p]
myWrapper(X)


# Comment changer la valeur de a et b ?
#
# Impossible : les paramètres a et b sont codés *en dur*.
#

# ## Classe ParametricFunction
#
# La solution la plus simple est d’utiliser la classe ParametricFunction.
#
# On procède en deux étapes.
#
# Etape 1 : augmenter le nombre de variables d’entrée
#

# In[2]:


def ishigamiG(x):
    a = x[3]
    b = x[4]
    y = math.sin(x[0]) + a * math.sin(x[1]) ** 2 + b * x[2] ** 4 * math.sin(x[0])
    return [y]


myParamWrapper = ot.PythonFunction(5, 1, ishigamiG)


# In[3]:


X = [p, p, p, 7.0, 0.1]
myParamWrapper(X)


# Etape 2 : restreindre le nombre de variables, fixer les autres à une valeur
# de référence
#

# In[4]:


a = 7.0
b = 0.1
indices = [3, 4]
refPoint = [a, b]
myWrapper = ot.ParametricFunction(myParamWrapper, indices, refPoint)


# In[5]:


X = [p, p, p]
myWrapper(X)


# ## Classe OpenTURNSPythonFunction
#
# La solution la plus exaltante est de créer une nouvelle classe dérivée de la classe `Function`.
#
# Etape 1 : créer la classe
#

# In[6]:


class IshigamiFunction(ot.OpenTURNSPythonFunction):
    def __init__(self, a, b):
        super(IshigamiFunction, self).__init__(3, 1)
        self._a = a
        self._b = b

    def _exec(self, X):
        a = self._a
        b = self._b
        y = math.sin(X[0]) + a * math.sin(X[1]) ** 2 + b * X[2] ** 4 * math.sin(X[0])
        return [y]


# Etape 2 : Créer une NMF à partir d’icelle.
#

# In[7]:


a = 7.0
b = 0.1
myParametricWrapper = IshigamiFunction(a, b)
myWrapper = ot.Function(myParametricWrapper)


# In[8]:


X = [p, p, p]
myWrapper(X)


# ## Synthèse
#
# `ParametricFunction` :
# * Simple à utiliser
# * N’importe quel type de fonction peut être paramétrisée : symbolique, Python, ou autre
# * Permet d’activer/désactiver une variable aléatoire
# * Gère des nombres flottants, uniquement (ni entiers, ni chaînes de caractères)
#
# `OpenTURNSPythonFunction` :
# * Plus complexe (un peu)
# * Uniquement pour une fonction Python
# * Gère n’importe quel type de paramètres (flottants, entiers, chaînes de caractères, structures plus complexes)
#

# ## Exercices
#
# Le script `ParametricFun/testCrue-sujet.py` contient une implémentation du cas crue.
#

# In[9]:


def functionCrue(X):
    H_d = 3.0  # Hauteur de la digue
    Z_b = 55.5  # Cote de la berge
    L = 5.0e3  # Longueur de la riviere
    B = 300.0  # Largeur de la riviere
    Z_d = Z_b + H_d
    Q, K_s, Z_v, Z_m = X
    alpha = (Z_m - Z_v) / L
    H = (Q / (K_s * B * sqrt(alpha))) ** (3.0 / 5.0)
    Z_c = H + Z_v
    S = Z_c - Z_d
    return [S]


myWrapper = ot.PythonFunction(4, 1, functionCrue)


# Les paramètres `H_d`, `Z_b`, `L`, `B` sont codés en dur dans `functionCrue`.
#
# Dans les exercices qui suivent, on teste plusieurs techniques pour pouvoir modifier les paramètres `H_d`, `Z_b`, `L`, `B`.
#
# ## Exercice 1
#
# Créer un nouveau script `testCrue-parametrique.py` et utiliser la classe `ParametricFunction` pour créer une nouvelle fonction paramétrique.
#
# ## Exercice 2
#
# Créer un nouveau script `testCrue-classe.py` et utiliser la classe `OpenTURNSPythonFunction` pour créer une nouvelle fonction paramétrique.
#
# ## Exercice 3
#
# En pratique, à quoi pourrait servir de pouvoir disposer de cette fonction paramétrique ?
#
# Réponses aux questions dans :
# * ParametricFun/testCrue-parametricFun.py
# * ParametricFun/testCrue-classeOTPFun.py
