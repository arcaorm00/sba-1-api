from titanic.entity import Entity
import sys
sys.path.insert(0, '/Users/saltQ/sbaProject')
import pandas as pd
import numpy as np
# sklearn algorithm: classification, regression, clustring, reduction 
from sklearn.tree import DecisionTreeClassifier # dtree
from sklearn.ensemble import RandomForestClassifier # rforest
from sklearn.naive_bayes import GaussianNB # nb
from sklearn.neighbors import KNeighborsClassifier # knn
from sklearn.svm import SVC # svm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold # k값은 count의 의미로 이해
from sklearn.model_selection import cross_val_score
# dtree, rforest, nb, knn, svm