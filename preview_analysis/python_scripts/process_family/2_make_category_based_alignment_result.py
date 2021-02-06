import pandas as pd
import sys
import numpy as np

dataset = pd.read_csv(sys.argv[1])
name_output = sys.argv[2]

matrix_export = []

keys = ['fp_domain','nhr_domain','chr_domain','tm_domain','loop2','loop1']

for i in range(len(dataset)):
	row_data = []

	#get max value:
	row_values = []
	for key in keys:
		row_values.append(dataset[key][i])

	max_value = np.max(row_values)

	row_data.append(max_value)

	for j in range(len(keys)):
		if row_values[j] == max_value:
			row_data.append(keys[j])
			break

	#get rest of the information about the data
	row_data.append(dataset['sequence'][i])

	matrix_export.append(row_data)

data_export = pd.DataFrame(matrix_export, columns=["score", "domain", "sequence"])
data_export.to_csv(name_output, index=False)