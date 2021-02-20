import pandas as pd
import sys

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

matrix_data = []

relevant_keys = ['length','molecular_weigth','charge','charge_density','isoelectric','inestability','aromaticity','aliphatic_index','hydrophobic_ratio','hydrophobicity_profile','hydrophobic_profile','inhibition_IC50', 'categorized_IC50']

for i in range(len(dataset)):

	row = [dataset[key][i] for key in relevant_keys]
	matrix_data.append(row)

data_export = pd.DataFrame(matrix_data, columns=relevant_keys)

data_export = data_export.dropna()

data_export.to_csv(path_output+"dataset_with_properties.csv", index=False)
