import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np

def make_histogram_for_distance(data_values, name_output, name_feature):

	plt.clf()

	# An "interface" to matplotlib.axes.Axes.hist() method
	n, bins, patches = plt.hist(x=data_values, bins='auto', color='#0504aa',
	                            alpha=0.7, rwidth=0.85)
	plt.grid(axis='y', alpha=0.75)
	plt.xlabel('Value')
	plt.ylabel('Frequency')
	plt.title(name_feature)
	maxfreq = n.max()
	# Set a clean upper y-axis limit.
	plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)

	plt.savefig(name_output)

print("Process input file")

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]
filter_value = 500

print("Process cont")
cont_yes=0
cont_not=0

for i in range(len(dataset)):
	if dataset['inhibition_IC50'][i] >=filter_value:
		cont_yes+=1
	else:
		cont_not+=1

print("No pass filters: ", cont_yes, "Pass filters: ", cont_not)

print("Process histogram")
hist_data = [value for value in dataset['inhibition_IC50'] if value <filter_value]
make_histogram_for_distance(hist_data, path_output+"histogram_IC50.svg", "IC50")

hist_data = np.log2(hist_data)
make_histogram_for_distance(hist_data, path_output+"histogram_IC50_log_view.svg", "IC50")

print("Add column with filter response")
filter_data = []

for i in range(len(dataset)):
	if dataset['inhibition_IC50'][i] <=filter_value:
		
		row = [dataset[key][i] for key in dataset.keys()]
		filter_data.append(row)

dataset_export = pd.DataFrame(filter_data, columns=dataset.keys())
dataset_export.to_csv(path_output+"19_filter_data_by_values_IC50.csv", index=False)
