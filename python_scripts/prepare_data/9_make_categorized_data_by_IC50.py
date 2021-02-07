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

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

data_values = [value for value in dataset['inhibition_IC50'] if str(value) != "nan"]
#get statistical values
min_value = min(data_values)
max_value = max(data_values)
average_value = np.mean(data_values)
std_Data = np.std(data_values)
q1 = np.quantile(data_values, .25)
q3 = np.quantile(data_values, .75)

print("Min value: ", min_value)
print("Max value: ", max_value)
print("Average value: ", average_value)
print("STD value: ", std_Data)
print("Q1 value: ", q1)
print("Q3 value: ", q3)

ranges = {"0-10": 0, "10-100": 0, ">100": 0}

for i in range(len(data_values)):
	if data_values[i]>100:
		ranges[">100"]+=1
	elif data_values[i]<=100 and data_values[i]>10:
		ranges["10-100"]+=1
	else:
		ranges["0-10"]+=1

print(ranges)

print("Categorized dataset using proposal range")

categorized_IC50 = []

for i in range(len(dataset)):
	if dataset['inhibition_IC50'][i] >100:
		categorized_IC50.append("Class III")
	elif dataset['inhibition_IC50'][i]<=100 and dataset['inhibition_IC50'][i]>10:
		categorized_IC50.append("Class II")
	else:
		categorized_IC50.append("Class I")

dataset['categorized_IC50'] = categorized_IC50

dataset.to_csv(path_output+"14_update_dataset_add_IC50_categories.csv", index=False)
