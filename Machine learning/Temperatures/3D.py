import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_excel('temp.xlsx')

x = dataset.iloc[:, 0]
y = dataset.iloc[:, 1]
z = dataset.iloc[:, 2]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(x, y, z, color='blue')
ax.set_xlabel('Vent')
ax.set_ylabel('Température réelle')
ax.set_zlabel('Température ressentie')

plt.show()