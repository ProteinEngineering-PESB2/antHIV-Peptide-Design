import pandas as pd
import sys
from Bio import SeqIO
import numpy as np
import plotly.express as px

fasta_file = sys.argv[1]
path_output = sys.argv[2]

matrix_sequence = []

residues_sort = ["A","R","N","D","C","Q","E","G","H","I","L","K","M","F","P","S","T","W","Y","V", "-"]

print("Read fasta file")

consensus_sequences = []

#read fasta file
for record in SeqIO.parse(fasta_file, "fasta"):
	row = [record.id]

	for residue in record.seq:
		row.append(residue)		

	matrix_sequence.append(row)

print("Make analysis heat map by class values IC50")

for class_data in ["Class_I", "Class_II", "Class_III"]:
	try:
		print("Process data for class: ", class_data)

		matrix_data_class = []

		for i in range(len(matrix_sequence)):
			name_sequences = matrix_sequence[i][0].split(":")

			if name_sequences[-1] == class_data:
				matrix_data_class.append(matrix_sequence[i])

		print("Process data to export in csv format")
		header = ["id_sequence"]

		for i in range(len(matrix_data_class[0])-1):
			header.append("P_"+str(i+1))

		dataset_pandas = pd.DataFrame(matrix_data_class, columns=header)
		dataset_pandas.to_csv(path_output+class_data+"_multi_alignment_view.csv", index=False)

		print("Make summary alignment using all data by position")

		matrix_summary = []
		matrix_summary_not_residue = []

		for element in ["A","R","N","D","C","Q","E","G","H","I","L","K","M","F","P","S","T","W","Y","V", "-"]:
			
			row = [element]
			row_not = []

			for key in header:

				if key != "id_sequence":
					cont=0
					for i in range(len(dataset_pandas)):
						if dataset_pandas[key][i] == element:
							cont+=1

					percentage = round(cont*100/len(dataset_pandas),2)
					row.append(percentage)
					row_not.append(percentage)

			matrix_summary.append(row)
			matrix_summary_not_residue.append(row_not)

		header2 = ["residue"]
		header2_not = []

		for i in range(len(matrix_sequence[0])-1):
			header2.append("P_"+str(i+1))
			header2_not.append("P_"+str(i+1))

		data_summary = pd.DataFrame(matrix_summary, columns=header2)
		data_summary.to_csv(path_output+class_data+"_summary_elements_by_position.csv", index=False)

		print("Process heatmap for alignment")

		fig = px.imshow(matrix_summary_not_residue,
		                labels=dict(x="Relative Positions", y="Residues", color="Frequency"),
		                x=header2_not,
		                y=["A","R","N","D","C","Q","E","G","H","I","L","K","M","F","P","S","T","W","Y","V", "-"]
		               )
		fig.update_xaxes(side="top")

		fig.update_layout(    
		    width=2100,
		    height=2100        
		)
		fig.write_image(path_output+class_data+"_heatmap_alignment_summary.svg")

		print("Creating relative consensus sequence")

		sequence_consensus = [class_data]
		sequence_consensus_value = [class_data]

		for key in header2_not:

			max_value_index = -1
			max_value = -1

			for i in range(len(data_summary)):

				if data_summary[key][i]>=max_value:
					max_value=data_summary[key][i]
					max_value_index=i

			sequence_consensus.append(residues_sort[max_value_index])
			sequence_consensus_value.append(max_value)

		consensus_sequences.append(sequence_consensus)
		consensus_sequences.append(sequence_consensus_value)
	except:
		pass
header_export_consensus = ["class"]
for i in range(len(consensus_sequences[0])-1):
	header_export_consensus.append("P_"+str(i+1))

data_sequences_export = pd.DataFrame(consensus_sequences, columns=header_export_consensus)
data_sequences_export.to_csv(path_output+"summary_consensus_sequences_residues.csv", index=False)

