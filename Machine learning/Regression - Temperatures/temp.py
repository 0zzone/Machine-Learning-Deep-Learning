# On importe les librairies
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split 
from math import *

# Pour gérer un warning (si vous en avez un)
import warnings
warnings.filterwarnings("ignore")

# On charge le dataset
dataset = pd.read_excel('temp.xlsx')

params = dataset.iloc[:, :-1] # On récupère la première et deuxième colonne
res = dataset.iloc[:, -1] # On récupère la dernière colonne

# On sépare notre jeu de données d'entraînement et de test
x_train, x_test, y_train, y_test = train_test_split(params, res, test_size=0.2, random_state=0)

Regressor = LinearRegression()
Regressor.fit(x_train, y_train) # On entraine notre modèle
y_pred = Regressor.predict(x_test) # On lance notre modèle sur notre jeu de test

plt.scatter(y_pred, y_test) # On compare les données de test et de prédiction (si =, alors c'est bien)
plt.xlabel('Valeurs de prédiction')
plt.ylabel('Valeurs de test')

# On demande et on calcule la température ressentie à partir du vent de de la température réelle demandée à l'utilisateur
vent = int(input('Quelle est la vitesse du vent ? '))
temp = int(input('Quelle est la température réelle ? '))
y = Regressor.predict([[vent, temp]])
print(f"La température ressentie sera de {round(y[0], 2)}")

plt.show()