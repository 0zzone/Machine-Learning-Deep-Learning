import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
from math import *

dataset = pd.read_excel('AnglesRotation.xls')

x = dataset.iloc[:, :-1]
y = dataset.iloc[:, -1]


Regressor = LinearRegression()
Regressor.fit(x, y)
y_pred = Regressor.predict(x)

def predire(tab):
	""" This function returns the angle """
	res = Regressor.predict([tab])
	return res[0]

