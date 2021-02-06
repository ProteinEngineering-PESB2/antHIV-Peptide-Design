import pandas as pd
import sys
import os

classify_sequences = pd.read_csv(sys.argv[1])
dataset_full = pd.read_csv(sys.argv[2])
path_output = sys.argv[3]

print("Process domains")
unique_class_domain = list(set(classify_sequences['domain']))

for domain in unique_class_domain:

	print("Create dir: ", domain)

	command = "mkdir -p " +path_output+domain
	print(command)
	os.system(command)

	print("Get sequences")
	#get sequences classified on this domain
	sequences = [classify_sequences['sequence'][i] for i in range(len(classify_sequences)) if classify_sequences['domain'][i] == domain]

	print("Get information about sequences using full dataset")

	matrix_information = [dataset_full.iloc[i] for i in range(len(dataset_full)) if dataset_full['sequence'][i] in sequences]
	
	print("Export data sequences")
	data_export = pd.DataFrame(matrix_information, columns=dataset_full.keys())

	data_export.to_csv(path_output+domain+"/dataset_per_domain_"+domain+".csv", index=False)	


