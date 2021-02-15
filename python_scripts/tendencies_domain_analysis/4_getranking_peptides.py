import pandas as pd
import sys

dataset = pd.read_csv(sys.argv[1])
data_categorized = pd.read_csv(sys.argv[2])
path_output = sys.argv[3]

print("Merge datasets")

data_merged = pd.merge(dataset, data_categorized, on="sequence")

print("Filter sequences by class")

for class_data in ["Class I", "Class II", "Class III"]:

	print("Process class: ", class_data)
	matrix_data = []

	for i in range(len(data_merged)):
		if data_merged['categorized_IC50'][i] == class_data:
			row = [data_merged[key][i] for key in data_merged.keys()]
			matrix_data.append(row)

	data_category = pd.DataFrame(matrix_data, columns=data_merged.keys())

	print("Sort by IC50")

	data_category = data_category.sort_values(by=['inhibition_IC50'])
	data_category.to_csv(path_output+"sort_data_by_IC50_"+class_data+".csv", index=False)
