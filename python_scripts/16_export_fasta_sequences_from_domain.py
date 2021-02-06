import pandas as pd
import sys

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

index_sequences = []

for i in range(len(dataset)):

	index = "sequence_"+str(i+1)
	index_sequences.append(index)

dataset["id_sequence"] = index_sequences

export_fasta = open(path_output+"fasta_sequences.fasta", 'w')

for i in range(len(dataset)):
	export_fasta.write(">"+dataset["id_sequence"][i]+"\n")

	if i == len(dataset)-1:
		export_fasta.write(dataset["sequence"][i])
	else:
		export_fasta.write(dataset["sequence"][i]+"\n")

export_fasta.close()
dataset.to_csv(path_output+"16_update_dataset_add_id_sequence.csv", index=False)

