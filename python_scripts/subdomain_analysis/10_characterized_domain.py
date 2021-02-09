import pandas as pd
import sys
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt
import plotly.express as px

dataset_input = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]
domain_to_evaluate = sys.argv[3]

#process dataset, selecting the features concerning the domain to evaluate
matrix_data = []

for i in range(len(dataset_input)):
	if dataset_input['domain'][i] == domain_to_evaluate:
		row = [dataset_input[key][i] for key in dataset_input.keys()]
		matrix_data.append(row)

dataset = pd.DataFrame(matrix_data, columns=dataset_input.keys())

#make statistical summary of relevant features to caracte
matrix_data_statistical = []

print("Process statistical summary")

for feature in ['length','molecular_weigth','charge','charge_density','isoelectric','inestability','aromaticity','aliphatic_index','hydrophobic_ratio','hydrophobicity_profile','hydrophobic_profile','inhibition_IC50']:

	print("Process feature: ", feature)

	min_value = np.min(dataset[feature])
	max_value = np.max(dataset[feature])
	avg_value = np.mean(dataset[feature])
	std_value = np.std(dataset[feature])
	q1_value = np.quantile(dataset[feature], .25)
	q3_value = np.quantile(dataset[feature], .75)

	row = [min_value, max_value, avg_value, std_value, q1_value, q3_value]
	matrix_data_statistical.append(row)

print("Export statistical summary")
dataset_statistical = pd.DataFrame(matrix_data_statistical, columns = ["min_value", "max_value", "avg_value", "std_value", "q1_value", "q3_value"])
dataset_statistical["feature"] = ['length','molecular_weigth','charge','charge_density','isoelectric','inestability','aromaticity','aliphatic_index','hydrophobic_ratio','hydrophobicity_profile','hydrophobic_profile','inhibition_IC50']
dataset_statistical.to_csv(path_output+"statistical_summary.csv", index=False)

#make correlation analisis
print("Process correlation matrix data")
dataset_analysis = pd.DataFrame()

for feature in ['length','molecular_weigth','charge','charge_density','isoelectric','inestability','aromaticity','aliphatic_index','hydrophobic_ratio','hydrophobicity_profile','hydrophobic_profile','inhibition_IC50']:
	dataset_analysis[feature] = dataset[feature]

corrMatrix = dataset_analysis.corr()
corrMatrix.to_csv(path_output+"correlation_matrix.csv")

f, ax = plt.subplots(figsize=(12, 10))
sn.heatmap(corrMatrix, mask=np.zeros_like(corrMatrix, dtype=np.bool), cmap=sn.diverging_palette(220, 10, as_cmap=True),square=True, ax=ax, annot=True)
plt.savefig(path_output+"correlation_matrix.svg")

#make scatter plot using featurest of interest 
print("Process scatter plot matrix dataset")
dataset_analysis['categorized_IC50'] = dataset['categorized_IC50']

fig = px.scatter_matrix(dataset_analysis, dimensions=['length','molecular_weigth','charge','charge_density','isoelectric','inestability','aromaticity','aliphatic_index','hydrophobic_ratio','hydrophobicity_profile','hydrophobic_profile','inhibition_IC50'], color="categorized_IC50")

fig.update_layout(
    title='Scatter Plot Matrix',    
    width=2100,
    height=2100        
)

fig.write_image(path_output+"scatter_plot_matrix.svg")

#make parallel coordinates
print("Process parallel coordinates")

numerical_categories = []

for i in range(len(dataset_analysis)):
	if dataset_analysis['categorized_IC50'][i] == "Class III":
		numerical_categories.append(3)

	elif dataset_analysis['categorized_IC50'][i] == "Class II":
		numerical_categories.append(2)
	else:
		numerical_categories.append(1)

dataset_analysis["numerical_categories"]  = numerical_categories
print(dataset_analysis)
#'inhibition_IC50'
fig = px.parallel_coordinates(dataset_analysis, color="numerical_categories",  dimensions=['length','molecular_weigth','charge','charge_density','isoelectric','inestability','aromaticity','aliphatic_index','hydrophobic_ratio','hydrophobicity_profile','hydrophobic_profile','inhibition_IC50'], color_continuous_scale=px.colors.diverging.Tealrose, color_continuous_midpoint=2)
fig.update_layout(
    title='Parallel Coordinates curve',    
    width=2100,
    height=2100        
)


fig.write_image(path_output+"parallel_coordinates.svg")
