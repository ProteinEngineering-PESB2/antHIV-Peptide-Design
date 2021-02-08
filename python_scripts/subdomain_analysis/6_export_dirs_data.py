import pandas as pd
import sys
import os

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

index_sequences = ["seq_"+str(i+1) for i in range(len(dataset))]

dataset["id_sequence"] = index_sequences

domains = list(set(dataset['domain']))


for domain in domains:
	print("Process domain: ", domain)

	command = "mkdir -p %s%s" % (path_output, domain)
	print(command)
	os.system(command)

	export_fasta = open(path_output+domain+"/fasta_sequences.fasta", 'w')

	for i in range(len(dataset)):

		if dataset['domain'][i] == domain:
			id_sequence = ">"+dataset["id_sequence"][i]+":"+str(dataset['name_peptide'][i])+":"+str(dataset['inhibition_IC50'][i])+":"+str(dataset['categorized_IC50'][i])
			export_fasta.write(id_sequence+"\n")

			if i == len(dataset)-1:
				export_fasta.write(dataset["sequence"][i])
			else:
				export_fasta.write(dataset["sequence"][i]+"\n")

	export_fasta.close()

dataset.to_csv(sys.argv[1], index=False)