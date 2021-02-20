import pandas as pd
import numpy as np
import sys
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import cross_val_score
from joblib import dump, load
from sklearn.svm import LinearSVC, SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

matrix_response = []

print("Process file and split into data and response")

response = dataset['category_IC50']
matrix_data = dataset.drop(columns=["response_IC50", "category_IC50"])

#standardized data using min max scaler
print("Scaler dataset")
scaler = MinMaxScaler()
scaler.fit(matrix_data)
dataset_scaler = scaler.transform(matrix_data)

matrix_response = []

print("Exploring algorithms and hyperparameters")

print("Training predictive models with LinearSVC")
model=LinearSVC()
model.fit(dataset_scaler, response)
scores = cross_val_score(model, dataset_scaler, response, cv=10)	
print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

row = ["LinearSVC", "default", scores.mean(), scores.std(), np.max(scores)]
matrix_response.append(row)

print("Training predictive models with RandomForestClassifier")
for criterion in ["gini", "entropy"]:
	for n_estimators in [100, 150, 200, 250, 500, 1000]:
		model=RandomForestClassifier(n_estimators=n_estimators,criterion=criterion, n_jobs=-1)
		model.fit(dataset_scaler, response)
		scores = cross_val_score(model, dataset_scaler, response, cv=10)	
		print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

		params = criterion+"-"+str(n_estimators)
		row = ["RandomForestClassifier", params, scores.mean(), scores.std(), np.max(scores)]
		matrix_response.append(row)

print("Training predictive models with SVC")
model=SVC()
model.fit(dataset_scaler, response)
scores = cross_val_score(model, dataset_scaler, response, cv=10)	
print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

row = ["SVC", "default", scores.mean(), scores.std(), np.max(scores)]
matrix_response.append(row)

print("Training predictive models with SGDClassifier")
model=SGDClassifier()
model.fit(dataset_scaler, response)
scores = cross_val_score(model, dataset_scaler, response, cv=10)	
print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

row = ["SGDClassifier", "default", scores.mean(), scores.std(), np.max(scores)]
matrix_response.append(row)

print("Training predictive models with KNeighborsClassifier")
for n_neighbors in range(2, 15):
	for algorithm in ['auto', 'ball_tree', 'kd_tree', 'brute']:
		for weight in ['uniform', 'distance']:
			model=KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=algorithm, weights=weight, n_jobs=-1)
			model.fit(dataset_scaler, response)
			scores = cross_val_score(model, dataset_scaler, response, cv=10)	
			print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
			params = "%d-%s-%s" %(n_neighbors, algorithm, weight)
			row = ["KNeighborsClassifier", params, scores.mean(), scores.std(), np.max(scores)]
			matrix_response.append(row)

print("Training predictive models with GaussianProcessClassifier")
kernel = DotProduct() + WhiteKernel()
model=GaussianProcessClassifier(kernel=kernel,random_state=0)
model.fit(dataset_scaler, response)
scores = cross_val_score(model, dataset_scaler, response, cv=10)	
print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
row = ["GaussianProcessClassifier", "default", scores.mean(), scores.std(), np.max(scores)]
matrix_response.append(row)

print("Training predictive models with DecisionTreeClassifier")

for criterion in ["gini", "entropy"]:
	for splitter in ["best", "random"]:
		model=DecisionTreeClassifier(random_state=0, criterion=criterion, splitter=splitter)
		model.fit(dataset_scaler, response)
		scores = cross_val_score(model, dataset_scaler, response, cv=10)	
		print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
		
		params = "%s-%s" % (criterion, splitter)
		row = ["DecisionTreeClassifier", params, scores.mean(), scores.std(), np.max(scores)]
		matrix_response.append(row)

print("Training predictive models with BaggingClassifier")

for bootstrap in [True, False]:
	for n_estimators in [10, 50, 100, 150, 200, 250, 500, 1000]:

		model=BaggingClassifier(n_estimators=n_estimators, random_state=0, n_jobs=-1, bootstrap=bootstrap)
		model.fit(dataset_scaler, response)
		scores = cross_val_score(model, dataset_scaler, response, cv=10)	
		print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
		params = "%s-%s" % (str(n_estimators), str(bootstrap))
		row = ["BaggingClassifier", params, scores.mean(), scores.std(), np.max(scores)]
		matrix_response.append(row)

print("Training predictive models with AdaBoostClassifier")
for n_estimators in [10, 50, 100, 150, 200, 250, 500, 1000]:
	for algorithm in ["SAMME", "SAMME.R"]:

		model=AdaBoostClassifier(random_state=0, n_estimators=n_estimators, algorithm=algorithm)
		model.fit(dataset_scaler, response)
		scores = cross_val_score(model, dataset_scaler, response, cv=10)
		params = "%d-%s" % (n_estimators, algorithm)
		print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
		row = ["AdaBoostClassifier", params, scores.mean(), scores.std(), np.max(scores)]
		matrix_response.append(row)

print("Training predictive models with GradientBoostingClassifier")

for loss in ["deviance"]:
	for n_estimators in [10, 50, 100, 150, 200, 250, 500, 1000]:
		for criterion in ["friedman_mse", "mse", "mae"]:
			model=GradientBoostingClassifier(random_state=0, loss=loss, n_estimators=n_estimators, criterion=criterion)
			model.fit(dataset_scaler, response)
			scores = cross_val_score(model, dataset_scaler, response, cv=10)	
			print("%0.2f r_score with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
			
			params = "%s-%d-%s" % (loss, n_estimators, criterion)
			row = [ "GradientBoostingClassifier", params, scores.mean(), scores.std(), np.max(scores)]
			matrix_response.append(row)

print("Export data summary")
data_export = pd.DataFrame(matrix_response, columns=["algorithm", "hyperparameters", "average", "std", "max_performance"])
data_export.to_csv(path_output+"summary_performance.csv", index=False)