#!/usr/bin/env python
# coding: utf-8

# # Wrappers - Fonction symbolique
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

# # Déroulement
#
# 9h30 - 11h (1h30)
# * Introduction : 5 min
# * Fonction Python : 45 min
# * Fonction symbolique : 45 min
#
# 11h - 12h30 (1h30)
# * Coupling Tools : 45 min
# * Fonction paramétriques : 15 min
# * Synthèse : 5 min

# ## Résumé
#
# Dans cette page, nous présentons la fonction symbolique et ses fonctionnalités. Les exercices associés explorent les thèmes du calcul du gradient.

# ## Références
#
# * User Manual, Functions : http://openturns.github.io/openturns/master/user_manual/functions.html
# * Examples, Functional modeling : http://openturns.github.io/openturns/master/examples/functional_modeling/functional_modeling.html
#
# * http://openturns.github.io/openturns/master/user_manual/_generated/openturns.MemoizeFunction.html
# * Sur ExprTk : OpenTURNS Users’ Day #11, Friday, the 15 th, June 2018, Denis Barbier, http://trac.openturns.org/blog/OpenTURNS_Users_Day_11

# ## Fonction symbolique : objectifs, avantages, inconvénients
#
# La classe `SymbolicFunction` peut créer des fonctions analytiques :
# * Idée : utiliser une fonction analytique simple.
# * Principe : fournir une chaîne de caractère définissant le calcul.
#
# Avantages :
# * Amélioration de la performance.
# * Calcul automatique du gradient exact, de la Hessienne exacte
#
# Inconvénients :
# * Nécessite une formule mathématique simple, typiquement une seule ligne.
#

# ## Fonction symbolique : prototype
#
# Prototype :
#
# `
# myWrapperAnalytical = SymbolicFunction (liste-des-entrees ,liste-des-formules )
# `
#
# où
# * liste-des-entrees : une liste de nbInputs chaînes de caractères, le nom des variables d’entrées
# * liste-des-formules : une liste de nbOutputs chaînes de caractères, les formules de calcul.

# In[1]:


import openturns as ot

X0 = ot.Normal(0.0, 1.0)
X1 = ot.Normal(0.0, 1.0)
X2 = ot.Normal(0.0, 1.0)
inputDistribution = ot.ComposedDistribution((X0, X1, X2))
inputRandomVector = ot.RandomVector(inputDistribution)


# In[2]:


myWrapper = ot.SymbolicFunction(("x0", "x1", "x2"), ("x0+x1+x2", "x0-x1*x2"))


# In[3]:


outputVect = ot.RandomVector(myWrapper, inputRandomVector)
montecarlosize = 10000
outputSample = outputVect.getSample(montecarlosize)
empiricalMean = outputSample.computeMean()
print(empiricalMean)


# ## Exercices

# ### Exercice 1 : fonction symbolique avec 4 entrées
#
# On considère le modèle :
# $$
# \begin{eqnarray}
# Y_1 &=& X_1 + X_2 + X_3 \\
# Y_2 &=& X_1 − X_2 X_3 \\
# Y_3 &=& 2 X_1 + 3 X_2 + 4 X_4
# \end{eqnarray}
# $$
#
# **Questions**
# * Créer une fonction symbolique pour créer ce nouveau modèle.
# * Evaluer la sortie du modèle au point $X=(1,2,3,4)^T$.
# * Estimer la moyenne de la sortie par Monte-Carlo simple.
#
# **Solution**
# * A la fin du présent Notebook.

# ### Exercice 2 : fonction symbolique avec paramètres
#
# On considère le modèle
# $$
# \begin{eqnarray}
# Y_1 &=& a X_1 + b X_2 \\
# Y_2 &=& c X_1 + d X_2
# \end{eqnarray}
# $$
# où a, b, c, d sont des paramètres :
# ```
# a = 12
# b = 23
# c = -34
# d = 45
# ```
#
# **Questions**
# * Créer une fonction symbolique pour créer ce nouveau modèle en utilisant la fonction `str`.
# * Evaluer la sortie du modèle au point $X=(1,2,3,4)^T$.
#
# Note : la classe `ParametricFunction` est plus adaptée pour cela.
#
# **Solution**
# * A la fin du présent Notebook.

# ### Exercice 3 : gradient d'une fonction symbolique
#
# On souhaite vérifier que OT peut calculer la dérivée formelle d’une
# fonction symbolique.
#
# **Questions**
# * Définir la fonction myWrapperSymbolic comme dans l’exemple fil rouge.
# * Créer la variable `myGradient` contenant la dérivée exacte du wrapper. Pour cela, utiliser la méthode `getGradient` de l’objet
# `myWrapperSymbolic`.
#
# * Qu’est-ce qui s’affiche quand on utilise l’instruction suivante ?
#
# `
# print(myGradient)
# `
#
# * On souhaite évaluer le gradient au point d’entrée suivant :
# `
# X = (1, 2, 3)
# `
# Utiliser la méthode `gradient` de l’objet `myGradient` pour évaluer G'(x).
#
# **Solution**
# * A la fin de ce notebook.

# ### Exercice 4 : gestion des variables intermédiaires dans une fonction symbolique
#
# Depuis OT 1.11, on peut définir une fonction symbolique dont l'évaluation est fondée sur des valeurs intermédiaires. Ainsi, la sortie n'est pas seulement une fonction explicite des entrées : on peut définir des résultats intermédiaires et les réutiliser dans une ou plusieurs sorties de la fonction.
#
# Pour cela, il faut utiliser la séquence d'appel suivante :
# ```
# myFunction = ot.SymbolicFunction(inputs, outputs, formula)
# ```
# où `outputs` est une chaîne de caractères contenant l'expression à évaluer.
#
# Pour composer cette chaîne de caractère, on peut définir plusieurs expressions, séparées par le caractère ";". De plus, les variables intermédiaires doivent être précédées du mot-clé "`var`".
#
# Par exemple, dans le cas du modèle dont les entrées sont $X_1$ et $X_2$ et les sorties sont $Y_1$ et $Y_2$ :
# $$
# \begin{eqnarray}
# T &=& X_1 X_2 \\
# Y_1 &=& X_1 + T \\
# Y_2 &=& X_2 − 3T
# \end{eqnarray}
# $$
# on peut utiliser l'instruction suivante :

# In[4]:


inputs = ["X1", "X2"]
formula = "var T := X1*X2; Y1 := X1+T; Y2 := X2-3*T"
outputs = ["Y1", "Y2"]
myFunction = ot.SymbolicFunction(inputs, outputs, formula)
myFunction([1.0, 2.0])


# Pour illustrer cette fonctionnalité, on considère le cas crue.
#
# On considère les 8 variables d'entrée suivantes :
# * Q : le débit de la rivière (m3/s)
# * Ks : le coefficient de Strickler (m1/3/s)
# * Zv : la côte du fond de la rivière en aval (m)
# * Zm : la côte du fond de la rivière en amont (m)
# * La hauteur de la digue : Hd = 3.0
# * La côte de la berge Zb = 55.5
# * La longueur du tronçon de rivière L = 5000
# * La largeur de la rivière B = 300.0
#
# On considère deux variables de sortie :
# * la hauteur de l'eau H,
# * la surverse S.
#
# Le lien entre les entrées et les sorties est donné par les équations suivantes.
#
# La pente de la rivière est :
# $$
# \alpha = \frac{Z_m - Z_v}{L}
# $$
# La hauteur de l'eau est modélisée par :
# $$
# H = \left(\frac{Q}{K_s B \sqrt{\alpha}}\right)^{0.6}
# $$
# La côte de la crue est :
# $$
# Z_c = H + Z_v
# $$
# La côte de la digue est :
# $$
# Z_d = Z_b + H_d
# $$
# La surverse est :
# $$
# S = Z_c - Z_d
# $$
#
# **Questions**
# * Utiliser les équations précédentes pour définir la fonction symbolique correspondante.
#
# **Solution**
# * A la fin du présent Notebook.

# ## Solution des exercices

# ### Solution de l'exercice 1 : fonction symbolique avec 4 entrées

# In[5]:


myWrapperSymbolic4 = ot.SymbolicFunction(
    ("x0", "x1", "x2", "x3"), ("x0+x1+x2", "x0-x1*x2", "2*x0+3*x1+4*x3")
)
X = ot.Point([1, 2, 3, 4])
Y = myWrapperSymbolic4(X)
Y


# In[6]:


X1 = ot.Normal(0.0, 1.0)
X2 = ot.Normal(0.0, 1.0)
X3 = ot.Normal(0.0, 1.0)
X4 = ot.Normal(0.0, 1.0)
inputDistribution = ot.ComposedDistribution((X1, X2, X3, X4))
inputRandomVector = ot.RandomVector(inputDistribution)
outputVect = ot.RandomVector(myWrapperSymbolic4, inputRandomVector)
montecarlosize = 10000
outputSample = outputVect.getSample(montecarlosize)
empiricalMean = outputSample.computeMean()
print(empiricalMean)


# ### Solution de l'exercice 2 : fonction symbolique avec paramètres

# In[7]:


a = 12
b = 23
c = -34
d = 45
y1str = str(a) + "*x0+" + str(b) + "*x1"
print(y1str)
y2str = str(c) + "*x0+" + str(d) + "*x1"
print(y2str)


# In[8]:


myWrapperABCD = ot.SymbolicFunction(("x0", "x1"), (y1str, y2str))
X = ot.Point([1, 2])
Y = myWrapperABCD(X)
Y


# ### Solution de l'exercice 3 : gradient d'une fonction symbolique

# In[9]:


myWrapper = ot.SymbolicFunction(("x0", "x1", "x2"), ("x0+x1+x2", "x0-x1*x2"))
print(myWrapper)
#
myGradient = myWrapper.getGradient()
print(myGradient)
#
myGradient.gradient([1.0, 2.0, 3.0])


# ### Solution de l'exercice 4 : gestion des variables intermédiaires dans une fonction symbolique

# In[10]:


import openturns as ot

Q = 1013.0
Ks = 30.0
Zv = 50.0
Zm = 55.0
Hd = 8
Zb = 55.5
L = 5000
B = 300
X = [Q, Ks, Zv, Zm, Hd, Zb, L, B]
X


# In[12]:


inputs = ["Q", "Ks", "Zv", "Zm", "Hd", "Zb", "L", "B"]
f1 = "var alpha := (Zm - Zv)/L"
f2 = "H := (Q/(Ks*B*sqrt(alpha)))^(3.0/5.0)"
f3 = "var Zc := H + Zv"
f4 = "var Zd := Zb + Hd"
f5 = "S := Zc - Zd"
# Concatène les chaînes de caractère avec le caractère ";" comme séparateur
formula = f1 + ";" + f2 + ";" + f3 + ";" + f4 + ";" + f5
print(formula)


# In[13]:


outputs = ["H", "S"]
myFunction = ot.SymbolicFunction(inputs, outputs, formula)
print(myFunction(X))
