import pandas as pd
import sys
import numpy as np
import os

import matplotlib.pyplot as plt

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

unique_domains = list(set(dataset['domain']))

#get statistics by domain by feature
for domain in unique_domains:
	command = "mkdir -p %s%s" % (path_output, domain)
	print(command)
	os.system(command)

	relevant_features = ['inhibition_IC50', 'length','molecular_weigth','charge','charge_density','isoelectric','inestability','aromaticity','aliphatic_index','hydrophobic_ratio','hydrophobicity_profile','hydrophobic_profile']

	mean_value = []
	std_value = []
	max_value = []
	min_value = []
	q1_value = []
	q3_value = []
	var_value = []

	for feature in relevant_features:
		row_value = []

		for i in range(len(dataset)):
			if dataset['domain'][i] == domain:
				if str(dataset[feature][i]) != "nan":				
					row_value.append(dataset[feature][i])				

		row_value = [value for value in row_value if str(value) != "nan"]
		if feature == "inhibition_IC50":
			print(row_value)
		#make histogram 
		make_histogram_for_distance(row_value, path_output+domain+"/"+feature+"_histogram.svg", feature)
		
		mean_value.append(np.mean(row_value))
		max_value.append(np.max(row_value))
		std_value.append(np.std(row_value))
		min_value.append(np.min(row_value))
		q1_value.append(np.quantile(row_value, .25))
		q3_value.append(np.quantile(row_value, .75))
		var_value.append(np.var(row_value))

	dataFrame = pd.DataFrame()
	dataFrame['feature'] = relevant_features
	dataFrame['mean_value'] = mean_value
	dataFrame['var_value'] = var_value
	dataFrame['std_value'] = std_value
	dataFrame['min_value'] = min_value
	dataFrame['max_value'] = max_value
	dataFrame['q1_value'] = q1_value
	dataFrame['q3_value'] = q3_value

	dataFrame.to_csv(path_output+domain+"/statistics_features.csv", index=False)