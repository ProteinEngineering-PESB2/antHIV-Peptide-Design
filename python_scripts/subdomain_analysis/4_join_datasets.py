import pandas as pd
import sys

dataset_full = pd.read_csv(sys.argv[1])
dataset_class = pd.read_csv(sys.argv[2])
path_output = sys.argv[3]

matrix_data = []

for i in range(len(dataset_full)):
	
	print("Process sequence ", i)	
	row = [dataset_full[key][i] for key in dataset_full.keys()]

	for j in range(len(dataset_class)):
		if dataset_class['sequence'][j] == dataset_full['sequence'][i]:
			
			for key in dataset_class.keys():
				if key != 'sequence':
					row.append(dataset_class[key][j])
			break

	matrix_data.append(row)

print("Export dataset")
header = [key for key in dataset_full.keys()]
header.append("score")
header.append("domain")

dataset_export = pd.DataFrame(matrix_data, columns=header)
dataset_export.to_csv(path_output+"4_merged_datasets_add_domain.csv", index=False)