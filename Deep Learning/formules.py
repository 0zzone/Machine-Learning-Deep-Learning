import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.metrics import accuracy_score
from utilities import *
from tqdm import tqdm

def initialisation(X):
	W = np.random.randn(X.shape[1], 1)
	b = np.random.randn(1)
	return (W, b)

def model(X, W, b):
	Z = X.dot(W) + b
	return 1/(1 + np.exp(-Z))

def log_loss(A, y):
	epsilon = 1e-15
	return 1/len(y) * np.sum(-y * np.log(A + epsilon) - (1 - y) * np.log(1 - A + epsilon))

def gradients(A, X, y):
	dW = 1/len(y) * np.dot(X.T, A - y)
	db = 1/len(y) * np.sum(A - y)
	return (dW, db)

def update(dW, db, W, b, alpha):
	W = W - alpha * dW
	b = b - alpha * db
	return (W, b)

def predict(X, W, b):
	A = model(X, W, b)
	return A >= 0.5

def artificial_neuron(X_train, y_train, X_test, y_test, alpha=0.01, n_iteration=10000):
	W, b = initialisation(X_train)

	train_loss = []
	test_loss = []

	train_acc = []
	test_acc = []

	for i in tqdm(range(n_iteration)):
		A = model(X_train, W, b)

		if i % 10 == 0:
			# Train
			train_loss.append(log_loss(A, y_train))
			y_pred = predict(X_train, W, b)
			train_acc.append(accuracy_score(y_train, y_pred))

			# Test
			A_test = model(X_test, W, b)
			test_loss.append(log_loss(A_test, y_test))
			y_pred = predict(X_test, W, b)
			test_acc.append(accuracy_score(y_test, y_pred))

		dW, db = gradients(A, X_train, y_train)
		W, b = update(dW, db, W, b, alpha)

	plt.figure(figsize=(12, 4))

	plt.subplot(1,2,1)
	plt.title('Log Loss function')
	plt.plot(train_loss, label="train loss")
	plt.plot(test_loss, label="test loss")
	plt.legend()

	plt.subplot(1,2,2)
	plt.title('Accuracy score evolution')
	plt.plot(train_acc, label="train accuracy")
	plt.plot(test_acc, label="test accuracy")
	plt.legend()

	plt.show()

	return (W, b)





















