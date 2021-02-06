import pandas as pd
import sys

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

domains = list(set(dataset['domain']))

for domain in domains:

	print("Process domain: ", domain)
	list_sequences = []
	list_names = []

	for i in range(len(dataset)):
		if dataset['domain'][i] == domain:
			list_sequences.append(dataset['sequence'][i])
			list_names.append(dataset['name_peptide'][i])

	#export data
	file_export = open(path_output+domain+"/"+domain+".fasta", 'w')

	for j in range(len(list_names)):
		file_export.write(">"+list_names[j]+"\n")
		file_export.write(list_sequences[j]+"\n")

	file_export.close()
