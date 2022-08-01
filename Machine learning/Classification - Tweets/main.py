import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

dataset = pd.read_csv('corona.csv')
df = pd.DataFrame(dataset)

df['Location'] = df['Location'].astype(float)

print(df.dtypes)

"""
x = df.iloc[:, 2:-1]
y = df.iloc[:, -1]

Logistic = LogisticRegression()
Logistic.fit(x, y)
"""