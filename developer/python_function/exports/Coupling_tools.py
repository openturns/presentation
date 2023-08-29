#!/usr/bin/env python
# coding: utf-8

# # Coupling Tools
#
# **Coding party OpenTURNS, march 2023**
#
# _Michaël Baudin_
#

# ## Résumé
#
# Dans cette page, nous présentons les fonctions du module `coupling_tools`, un module utile pour connecter un code de calcul fondé sur des échanges de fichiers texte. Nous présentons les principales fonctionnalités du module sur un exemple en particulier les fonctions `replace` et `get`.

# ## Références
#
# * http://openturns.github.io/openturns/master/developer_guide/wrapper_development.html
#

# ## Principe
#
# Le module coupling_tools est utile lorsque le code de calcul lit (en entrée) et écrit (en sortie) des fichiers texte.
#
# <img src="images/wrapper_OT-coupling.svg" width="600px">

# ## Fonctionnalités
#
# Principales fonctions du module `coupling_tools` :
# * `replace` : écrire un fichier d’entrée à partir d’un modèle, en remplaçant des balises par des valeurs
# * `execute` : exécuter un code de calcul externe
# * `get` (et `get_line_col`) : lire des valeurs à partir d’un fichier de sortie.
#
# Au-delà
# * Le module `coupling_tools` peut être utile en dehors d’OpenTURNS.
# * Exemple : « scripter » l’évaluation d’un plan d’expériences sur un serveur de calcul (cluster).

# ## Objectifs, Avantages, Inconvénients
#
# Les objectifs du module sont :
# * Lire/écrire des fichiers texte structurés (exemple : Code_Aster).
# * Simplicité : plus facile que les expressions régulières.
# * Sauter des lignes, des colonnes, des blocs de texte.
#
# Avantages :
# * Utile si les données d’entrée sont sous forme de fichier texte structuré.
#
# Inconvénients :
# * Facile à paralléliser, avec un peu plus de code Python (contacter si besoin).

# ## Exemple
#
# On a le code de calcul externe implémenté dans le script `external_program.py`. Ce programme :
# * lit le fichier `"input.py"`,
# * réalise le calcul et évalue la sortie,
# * écrit le fichier `"output.txt"`.
#
# La ligne de commande pour appeler le code est :
# ```
# python external_program.py input.py
# ```

# In[1]:


import openturns as ot
import openturns.coupling_tools as ct
import os

ot.__version__


# In[2]:


os.chdir("CouplingTools")


# Observons le contenu du script `external_program.py`.

# In[3]:


f = open("external_program.py", "r")
print(f.read())


# Observons le contenu du script `input.py` : le contenu est formatté en Python, pour faciliter la lecture.

# In[4]:


f = open("input.py", "r")
print(f.read())


# Le contenu du fichier `output.txt` est formatté de manière très simple.

# In[5]:


f = open("output.txt", "r")
print(f.read())


# Le fichier `input_template.py` est un modèle (*"template"*) qui va servir à générer le fichier `"input.py"`.

# In[6]:


f = open("input_template.txt", "r")
print(f.read())


# Le wrapper est implémenté ainsi : on fait d'abord appel à `replace` pour générer le fichier d'entrée, puis on appelle le code de calcul externe par une commande système avec la méthode `execute` et enfin on lit le fichier de sortie avec la méthode `get`.

# In[7]:


def mySimulator(X):
    # 1. Create input file
    infile = "input_template.txt"
    outfile = "input.py"
    tokens = ["@X0", "@X1", "@X2"]
    ct.replace(infile, outfile, tokens, X)
    # 2. Compute
    program = "python external_program.py"
    cmd = program + " " + outfile
    ct.execute(cmd)
    # 3. Parse output file
    Y = ct.get("output.txt", tokens=["Y0=", "Y1="])
    return Y


myWrapper = ot.PythonFunction(3, 2, mySimulator)


# In[8]:


X = [1.2, 45, 91.8]
Y = myWrapper(X)
Y


# ## Présentation de l'API
#
# Rentrons un peu plus dans le détail des fonctions.
#
# ### Ecriture du fichier d'entrée : la fonction replace
# ```
# replace (infile , outfile , tokens , values )
# ```
#
# Paramètres :
# * `infile` une chaîne de caractères, le fichier modèle à mettre à jour.
# * `outfile` une chaîne de caractères, le fichier à écrire.
# * `tokens` une liste de N éléments, les expressions régulières à rechercher.
# * `values` une liste de N éléments (chaînes, flottants,etc...), les valeurs à remplacer.

# In[9]:


X = [1.2, 45, 91.8]
infile = "input_template.txt"
outfile = "input.py"
tokens = ["@X0", "@X1", "@X2"]
ct.replace(infile, outfile, tokens, X)


# Pour voir le changement, il faut observer le contenu du script `input.py`.

# In[10]:


f = open("input.py", "r")
print(f.read())


# ### Lecture du fichier de sortie : la fonction get
#
# Séquence d’appel :
# ```Python
# # Recupere une liste de valeurs :
# Y = get (filename, tokens=None, skip_tokens=None , \
#          skip_lines=None , skip_cols= None )
# # Recupere une seule valeur :
# Y = get_value(filename, token=None, skip_token=0, \
#              skip_line=0, skip_col=0)
# ```
# Paramètres :
# * `filename` une chaîne de caractères, le fichier à lire
# * `tokens` une liste de N éléments, les expressions régulières à rechercher.
# * `skip_tokens` une liste de N éléments, le nombre de jetons à ignorer avant de lire la valeur.
# * `skip_lines` une liste de N éléments, le nombre de lignes à ignorer avant le jeton.
# * `skip_cols` une liste de N éléments, le nombre de colonnes à ignorer avant le jeton.
# * `Y` une liste de doubles (pour `get`) ou un double (pour `get_value`).

# ### Exemples d'utilisation de `get`
#
# Exemple avec saut de lignes/colonnes.
#
# Les trois premières lignes du fichier `results.txt` sont les suivantes :
# ```
# 1 2 3 04 5 6
# 7 8 9 10
# 11 12 13 14
# ```
#
# Objectif : Lire le 9.
#

# In[11]:


Y = ct.get_value("results.txt", skip_line=1, skip_col=2)
Y


# ## otwrapy
#
# * Module Python développé par Phiméca (hors partenariat) en complément de coupling_tools
# * https://github.com/openturns/otwrapy
# * Distribution des calculs possible via différents modules Python : multiprocessing (Python Standard Library), ipyparallel ou joblib.
# * Autres fonctionnalités : gestion des erreurs, création d’un répertoire temporaire de travail, écriture/lecture d’échantillon dans un fichier compressé, ...
#

# ## Autres modules
#
# Le langage Python, associé à sa librairie standard, est un langage de haut niveau très pratique et concis pour lire/écrire dans des fichiers, manipuler des chaînes de caractères ou lancer un processus (*thread*) ; si le module
# `coupling_tools` n’est pas adapté, ne pas oublier :
# * lecture fichiers texte :
#   * modules `re` (expressions régulières),
#   * méthodes `file.readline()`,
#   * `string.split()`,
#   * etc. ;
# * lecture fichier binaire HDF5 : module `h5py` (ou tables de `PyTables`) ;
# * lancement d’un calcul et parallélisme : modules `subprocess` et `multiprocessing`.
#

# ## Exercices

# ### Exercice 1
#
# * Quelles instructions Python "naïves" peut-on utiliser pour lire les valeurs X0, X1, X2 dans le fichier `input.py` ?
#
# * Dans le script `external_program.py`, pourquoi l'instruction suivante fonctionne-t-elle ?
# ```Python
# exec(open(inFile).read())
# ```

# ### Solution de l'exercice 1
#
# Cette instruction fonctionne car le fichier "input.py" est un script Python. C'est pourquoi l'instruction `exec` exécute la chaîne de caractère retournée par `open(inFile).read()`. Utiliser un script Python comme fichier d'entrée évite de développer un *parser*, associée à un langage spécifique.

# ### Exercice 2
#
# Changer le nom des variables :
# * X0 -> X1
# * X1 -> X2
# * X2 -> X3
#
# et adapter les scripts (lesquels ?).

# ### Exercice 3
#
# Le fichier `results.txt` contient les lignes suivantes :
# ```
# 1  2  3  04  5  6
# 7  8  9  10
# 11 12 13 14
#
# Y1= 11.11celcius
# Y2= -0.89
# Y1= 22.22
# Y1= 33.33
#
# line1: 100 101 102
# line2: 200 201 202
# line3: 300 301 302
# ```
# Comment utiliser la fonction `get_value` pour lire les valeurs
# suivantes dans le fichier results.txt ?
# * 11.11
# * 9.0
# * 201.0
# * 33.33
# * 22.22
# * 101.0
# * 300.0

# ### Solution de l'exercice 3

# In[12]:


filename = "results.txt"
# 1. search token, the value right after the token
# is returned:
Y = ct.get_value(filename, token="Y1=")  # 11.11
print("(1) Y:", Y)

# 2. skip lines and columns (useful for array search):
Y = ct.get_value(filename, skip_line=1, skip_col=2)  # 9
print("(2) Y:", Y)

# 3. skip lines and columns backward (be careful:
# if there is an empty line at the end of the file,
# it is taken into account. i.e. this last empty line
# will be reached using skip\_line=-1):
Y = ct.get_value(filename, skip_line=-2, skip_col=-2)  # 201
print("(3) Y:", Y)

# 4. search the 3rd appearance of the token:
Y = ct.get_value(filename, token="Y1=", skip_token=2)  # 33.33
print("(4) Y:", Y)

# 5. search the 2nd appearance of the token from the end
# of the file:
Y = ct.get_value(filename, token="Y1=", skip_token=-2)  # 22.22
print("(5) Y:", Y)

# 6. search a token and then skip lines and columns from
# this token:
Y = ct.get_value(filename, token="Y1=", skip_line=5, skip_col=-2)  # 101
print("(6) Y:", Y)

# 7. search the 2nd token and then skip lines and columns
# from this token:
Y = ct.get_value(filename, token="Y1=", skip_token=1, skip_line=5, skip_col=1)  # 300
print("(7) Y:", Y)


# ### Exercice 4
#
# La fonction `get_line_col` permet de lire des valeurs numériques dans une ligne ou une colonne.
#
# Considérons le fichier get_line_col.txt :
#
# ```
# 0
# 1
# 2
# 3
# 4
# 5
# 6  ; 2. 3   59.
# 7
# 8
# 9
# 10
#
# ```
#
# Utiliser la fonction `get_line_col` pour lire la valeur 59.
#
# Solution dans le script `get_line_col.py`

# ### Solution de l'exercice 4

# In[13]:


Y = ct.get_line_col("get_line_col.txt", skip_line=6, skip_col=4)
print("Y:", Y)
