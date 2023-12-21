import pandas as pd 
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

train=pd.read_excel("./leaf.xlsx")
y = train.Class
train.drop(['Class'], axis=1, inplace=True)
X = train

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=2)

DT= DecisionTreeClassifier()
DT.fit(X_train,y_train)

pred=DT.predict([[12,12]])
print(pred)
 
