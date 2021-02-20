import pandas as pd
import numpy as np
import sys
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import cross_val_score
from joblib import dump, load
from sklearn.svm import LinearSVR, SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import SGDRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

matrix_response = []

print("Process file and split into data and response")

response = dataset['response_IC50']
matrix_data = dataset.drop(columns=["response_IC50", "category_IC50"])

#standardized data using min max scaler
print("Scaler dataset")
scaler = MinMaxScaler()
scaler.fit(matrix_data)
dataset_scaler = scaler.transform(matrix_data)

matrix_response = []

print("Exploring algorithms and hyperparameters")

print("Training predictive models with LinearSVR")
model=LinearSVR()
model.fit(dataset_scaler, response)
scores = cross_val_score(model, dataset_scaler, response, cv=10)	
print("%0.2f r_score with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

row = ["LinearSVR", "default", scores.mean(), scores.std(), np.max(scores)]
matrix_response.append(row)


print("Training predictive models with RandomForestRegressor")
for criterion in ["mse", "mae"]:
	for n_estimators in [100, 150, 200, 250, 500, 1000]:
		model=RandomForestRegressor(n_estimators=n_estimators,criterion=criterion, n_jobs=-1)
		model.fit(dataset_scaler, response)
		scores = cross_val_score(model, dataset_scaler, response, cv=10)	
		print("%0.2f r_score with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

		params = criterion+"-"+str(n_estimators)
		row = ["RandomForestRegressor", params, scores.mean(), scores.std(), np.max(scores)]
		matrix_response.append(row)

print("Training predictive models with SVR")
model=SVR()
model.fit(dataset_scaler, response)
scores = cross_val_score(model, dataset_scaler, response, cv=10)	
print("%0.2f r_score with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

row = ["SVR", "default", scores.mean(), scores.std(), np.max(scores)]
matrix_response.append(row)

print("Training predictive models with SGDRegressor")
model=SGDRegressor()
model.fit(dataset_scaler, response)
scores = cross_val_score(model, dataset_scaler, response, cv=10)	
print("%0.2f r_score with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

row = ["SGDRegressor", "default", scores.mean(), scores.std(), np.max(scores)]
matrix_response.append(row)


print("Training predictive models with KNeighborsRegressor")
for n_neighbors in range(2, 15):
	for algorithm in ['auto', 'ball_tree', 'kd_tree', 'brute']:
		for weight in ['uniform', 'distance']:
			model=KNeighborsRegressor(n_neighbors=n_neighbors, algorithm=algorithm, weights=weight, n_jobs=-1)
			model.fit(dataset_scaler, response)
			scores = cross_val_score(model, dataset_scaler, response, cv=10)	
			print("%0.2f r_score with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
			params = "%d-%s-%s" %(n_neighbors, algorithm, weight)
			row = ["KNeighborsRegressor", params, scores.mean(), scores.std(), np.max(scores)]
			matrix_response.append(row)
			break
		break
	break

print("Training predictive models with GaussianProcessRegressor")
kernel = DotProduct() + WhiteKernel()
model=GaussianProcessRegressor(kernel=kernel,random_state=0)
model.fit(dataset_scaler, response)
scores = cross_val_score(model, dataset_scaler, response, cv=10)	
print("%0.2f r_score with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
row = ["GaussianProcessRegressor", "default", scores.mean(), scores.std(), np.max(scores)]
matrix_response.append(row)

print("Training predictive models with DecisionTreeRegressor")

for criterion in ["mse", "friedman_mse", "mae"]:
	for splitter in ["best", "random"]:
		model=DecisionTreeRegressor(random_state=0, criterion=criterion, splitter=splitter)
		model.fit(dataset_scaler, response)
		scores = cross_val_score(model, dataset_scaler, response, cv=10)	
		print("%0.2f r_score with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
		
		params = "%s-%s" % (criterion, splitter)
		row = ["DecisionTreeRegressor", params, scores.mean(), scores.std(), np.max(scores)]
		matrix_response.append(row)

print("Training predictive models with BaggingRegressor")

for bootstrap in [True, False]:
	for n_estimators in [10, 50, 100, 150, 200, 250, 500, 1000]:

		model=BaggingRegressor(n_estimators=n_estimators, random_state=0, n_jobs=-1, bootstrap=bootstrap)
		model.fit(dataset_scaler, response)
		scores = cross_val_score(model, dataset_scaler, response, cv=10)	
		print("%0.2f r_score with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
		params = "%s-%s" % (str(n_estimators), str(bootstrap))
		row = ["BaggingRegressor", params, scores.mean(), scores.std(), np.max(scores)]
		matrix_response.append(row)

print("Training predictive models with AdaBoostRegressor")
for n_estimators in [10, 50, 100, 150, 200, 250, 500, 1000]:
	for loss in ["linear", "square", "exponential"]:

		model=AdaBoostRegressor(random_state=0, n_estimators=n_estimators, loss=loss)
		model.fit(dataset_scaler, response)
		scores = cross_val_score(model, dataset_scaler, response, cv=10)
		params = "%d-%s" % (n_estimators, loss)
		print("%0.2f r_score with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
		row = ["AdaBoostRegressor", params, scores.mean(), scores.std(), np.max(scores)]
		matrix_response.append(row)

print("Training predictive models with GradientBoostingRegressor")

for loss in ["ls", "lad", "huber", "quantile"]:
	for n_estimators in [10, 50, 100, 150, 200, 250, 500, 1000]:
		for criterion in ["friedman_mse", "mse", "mae"]:
			model=GradientBoostingRegressor(random_state=0, loss=loss, n_estimators=n_estimators, criterion=criterion)
			model.fit(dataset_scaler, response)
			scores = cross_val_score(model, dataset_scaler, response, cv=10)	
			print("%0.2f r_score with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
			
			params = "%s-%d-%s" % (loss, n_estimators, criterion)
			row = [ "GradientBoostingRegressor", params, scores.mean(), scores.std(), np.max(scores)]
			matrix_response.append(row)
			break
		break
	break

print("Export data summary")
data_export = pd.DataFrame(matrix_response, columns=["algorithm", "hyperparameters", "average", "std", "max_performance"])
data_export.to_csv(path_output+"summary_performance.csv", index=False)
