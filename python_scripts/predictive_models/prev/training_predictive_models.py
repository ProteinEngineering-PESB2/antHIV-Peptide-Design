import pandas as pd
import numpy as np
import sys
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.linear_model import SGDRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_score
from joblib import dump, load

path_dataset = sys.argv[1]

list_clusters = ["alpha-structure_group", "betha-structure_group", "energetic_group", "hydropathy_group", "hydrophobicity_group", "index_group", "secondary_structure_properties_group", "volume_group"]

matrix_response = []

for cluster in list_clusters:

	print("Process cluster: ", cluster)

	dataset = pd.read_csv(path_dataset+cluster+"/encoding_Data_frequency.csv")

	response = dataset['response']
	matrix_data = dataset.drop(columns=["response"])

	#standardized data using min max scaler
	print("Scaler dataset")
	scaler = MinMaxScaler()
	scaler.fit(matrix_data)
	dataset_scaler = scaler.transform(matrix_data)

	print("Training predictive models with RandomForestRegressor")
	model=RandomForestRegressor(n_estimators=100,criterion="mse", n_jobs=-1)
	model.fit(dataset_scaler, response)
	scores = cross_val_score(model, dataset_scaler, response, cv=10)	
	print("%0.2f r_score with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
	
	row = [cluster, "RandomForestRegressor", "default", scores.mean(), scores.std(), np.max(scores)]
	matrix_response.append(row)

	print("Training predictive models with SVR")
	model=SVR(C=1.0, epsilon=0.2)
	model.fit(dataset_scaler, response)
	scores = cross_val_score(model, dataset_scaler, response, cv=10)	
	print("%0.2f r_score with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
	
	row = [cluster, "SVR", "default", scores.mean(), scores.std(), np.max(scores)]
	matrix_response.append(row)

	print("Training predictive models with SGDRegressor")
	model=SGDRegressor(max_iter=1000, tol=1e-3)
	model.fit(dataset_scaler, response)
	scores = cross_val_score(model, dataset_scaler, response, cv=10)	
	print("%0.2f r_score with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
	
	row = [cluster, "SGDRegressor", "default", scores.mean(), scores.std(), np.max(scores)]
	matrix_response.append(row)

	print("Training predictive models with KNeighborsRegressor")
	model=KNeighborsRegressor(n_neighbors=2)
	model.fit(dataset_scaler, response)
	scores = cross_val_score(model, dataset_scaler, response, cv=10)	
	print("%0.2f r_score with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
	
	row = [cluster, "KNeighborsRegressor", "default", scores.mean(), scores.std(), np.max(scores)]
	matrix_response.append(row)

	print("Training predictive models with GaussianProcessRegressor")
	kernel = DotProduct() + WhiteKernel()
	model=GaussianProcessRegressor(kernel=kernel,random_state=0)
	model.fit(dataset_scaler, response)
	scores = cross_val_score(model, dataset_scaler, response, cv=10)	
	print("%0.2f r_score with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
	
	row = [cluster, "GaussianProcessRegressor", "default", scores.mean(), scores.std(), np.max(scores)]
	matrix_response.append(row)

	print("Training predictive models with DecisionTreeRegressor")
	model=DecisionTreeRegressor(random_state=0)
	model.fit(dataset_scaler, response)
	scores = cross_val_score(model, dataset_scaler, response, cv=10)	
	print("%0.2f r_score with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
	
	row = [cluster, "DecisionTreeRegressor", "default", scores.mean(), scores.std(), np.max(scores)]
	matrix_response.append(row)

	print("Training predictive models with BaggingRegressor")
	model=BaggingRegressor(n_estimators=10, random_state=0)
	model.fit(dataset_scaler, response)
	scores = cross_val_score(model, dataset_scaler, response, cv=10)	
	print("%0.2f r_score with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
	
	row = [cluster, "BaggingRegressor", "default", scores.mean(), scores.std(), np.max(scores)]
	matrix_response.append(row)

	print("Training predictive models with AdaBoostRegressor")
	model=AdaBoostRegressor(random_state=0, n_estimators=100)
	model.fit(dataset_scaler, response)
	scores = cross_val_score(model, dataset_scaler, response, cv=10)	
	print("%0.2f r_score with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
	
	row = [cluster, "AdaBoostRegressor", "default", scores.mean(), scores.std(), np.max(scores)]
	matrix_response.append(row)

	print("Training predictive models with GradientBoostingRegressor")
	model=GradientBoostingRegressor(random_state=0)
	model.fit(dataset_scaler, response)
	scores = cross_val_score(model, dataset_scaler, response, cv=10)	
	print("%0.2f r_score with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
	
	row = [cluster, "GradientBoostingRegressor", "default", scores.mean(), scores.std(), np.max(scores)]
	matrix_response.append(row)	

data_export = pd.DataFrame(matrix_response, columns=["property", "algorithm", "hyperparameters", "average", "std", "max_performance"])
data_export.to_csv(path_dataset+"summary_performance.csv", index=False)
