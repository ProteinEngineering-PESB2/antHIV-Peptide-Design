import pandas as pd
import sys

def search_sequence(dataset, sequence):

	index = -1

	for i in range(len(dataset)):
		if dataset['sequence'][i] == sequence:
			index=i
			break

	return index

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

print("Original size: ", len(dataset))
sequence_data = list(set(dataset['sequence']))

matrix_data = []

for sequence in sequence_data:
	index = search_sequence(dataset, sequence)

	#ignore status data
	if dataset['status_filter'][index] == 0:
		row = [dataset[key][index] for key in dataset.keys()]
		matrix_data.append(row)

print("Final size: ", len(matrix_data))
dataset_export = pd.DataFrame(matrix_data, columns=dataset.keys())
dataset_export.to_csv(path_output+"filter_selected_sequences.csv", index=False)
