import pandas as pd
import sys
from Bio import SeqIO
import numpy as np
import plotly.express as px

fasta_file = sys.argv[1]
path_output = sys.argv[2]

matrix_sequence = []

print("Read fasta file")
#read fasta file
for record in SeqIO.parse(fasta_file, "fasta"):
	row = [record.id]

	for residue in record.seq:
		row.append(residue)		

	matrix_sequence.append(row)

print("Process data to export in csv format")
header = ["id_sequence"]

for i in range(len(matrix_sequence[0])-1):
	header.append("P_"+str(i+1))

dataset_pandas = pd.DataFrame(matrix_sequence, columns=header)
dataset_pandas.to_csv(path_output+"multi_alignment_view.csv", index=False)

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
data_summary.to_csv(path_output+"summary_elements_by_position.csv", index=False)

print("Process heatmap for alignment")

fig = px.imshow(matrix_summary_not_residue,
                labels=dict(x="Positions", y="Residues", color="Viridis"),
                x=header2_not,
                y=["A","R","N","D","C","Q","E","G","H","I","L","K","M","F","P","S","T","W","Y","V", "-"]
               )
fig.update_xaxes(side="top")

fig.update_layout(    
    width=2100,
    height=2100        
)
fig.write_image(path_output+"heatmap_alignment_summary.svg")
