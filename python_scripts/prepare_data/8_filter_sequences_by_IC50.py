import pandas as pd
import sys

print("Read data from csv file")
dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

print("Process filters data")
filter_value = 1000

cont_filters = 0
cont_not_values = 0

matrix_values_get = []

for i in range(len(dataset)):

	if dataset['inhibition_IC50'][i] < filter_value:
		cont_filters+=1

		row = [dataset[key][i] for key in dataset.keys()]
		matrix_values_get.append(row)

	else:
		cont_not_values+=1

print("Considered values: ", cont_filters)
print("Non Considered values: ", cont_not_values)

#export data to csv file
print("Export data to csv file")
data_export = pd.DataFrame(matrix_values_get, columns=dataset.keys())
data_export.to_csv(path_output+"8_filtered_sequences_by_IC50.csv", index=False)
