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

print("Process data")
dataset_JAH = pd.read_csv(sys.argv[1])
dataset_HIV = pd.read_excel(sys.argv[2], sheet_name="Sheet1")
path_output = sys.argv[3]

#get sequences in both databases
sequences_JAH = list(set(dataset_JAH['sequence']))
sequences_HIV = list(set(dataset_HIV['SEQUENCE']))

print("Get repeat sequences")
merge_sequences = [sequence for sequence in sequences_JAH if sequence in sequences_HIV]

#make dataframe using only unique sequences
sequences_data = []

print("Create unique data sequences")
for sequence in sequences_JAH:
	sequences_data.append([sequence, len(sequence), "DB_JAH"])

#adding filters related to target
for i in range(len(dataset_HIV)):

	if dataset_HIV['TARGET'][i] in ["Virus entry", "Fusion inhibitor"]:
		sequences_data.append([dataset_HIV['SEQUENCE'][i], len(dataset_HIV['SEQUENCE'][i]), "DB_HIV"])

#add repeat sequences
for sequence in merge_sequences:
	sequences_data.append([sequence, len(sequence), "repeat"])

data_sequences = pd.DataFrame(sequences_data, columns=["sequence", "length", "provide"])

print("Create histogram for length sequences")

#make histogram about length
make_histogram_for_distance(data_sequences['length'], path_output+"length_histogram.jpg", "Length")

print("Filter by length")

q1 = np.quantile(data_sequences['length'], .25)
q3 = np.quantile(data_sequences['length'], .75)

IQR = q3-q1

low_data = q1-1.5*IQR
high_data = q3+1.5*IQR
print(low_data)
print(high_data)

status_filters = []
cont=0
for i in range(len(data_sequences)):

	if data_sequences['length'][i]>=low_data and data_sequences['length'][i]<=high_data:
		status_filters.append(0)
	else:
		status_filters.append(1)
		cont+=1

print(len(data_sequences))
print(cont)
print(len(data_sequences)-cont)

data_sequences["status_filter"] = status_filters
data_sequences.to_csv(path_output+"selected_sequences.csv", index=False)