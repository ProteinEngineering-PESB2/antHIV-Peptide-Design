import pandas as pd
import sys 
import os
from scipy.fft import fft
import numpy as np

def encoding_sequence(sequence, value_property):

	#order in database
	array_residues = ['A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
	sequence_encoding = []

	for residue in sequence:		
		encoding_value =-1
		index=-1		
		for i in range(len(array_residues)):
			if array_residues[i] == residue:
				index=i
				break

		if index != -1:
			sequence_encoding.append(value_property[index])

	return sequence_encoding

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

#make encoding data
list_clusters = ["alpha-structure_group", "betha-structure_group", "energetic_group", "hydropathy_group", "hydrophobicity_group", "index_group", "secondary_structure_properties_group", "volume_group"]

for cluster in list_clusters:

	print(cluster)

	command = "mkdir -p "+path_output+cluster
	os.system(command)

	dataset_cluster = pd.read_csv(path_output+"encoding_AAIndex/"+cluster+"/data_component.csv")

	matrix_sequence_encoding = []
	length_data = []

	index_sequences = []
	index=0

	for i in range(len(dataset)):
		sequence = dataset['sequence'][i]		
		sequence_encoding = encoding_sequence(sequence, dataset_cluster['component_1'])		
		matrix_sequence_encoding.append(sequence_encoding)
		length_data.append(len(sequence_encoding))

	#make zero padding	
	for i in range(len(matrix_sequence_encoding)):
		for j in range(len(matrix_sequence_encoding[i]),max(length_data)):
			matrix_sequence_encoding[i].append(0)


	#make fast fourier
	print("Apply FFT to get frequency spectra")
	matrix_digitized = []

	for i in range(len(matrix_sequence_encoding)):

		T = 1.0/float(len(matrix_sequence_encoding[i]))
		x = np.linspace(0.0, len(matrix_sequence_encoding[i])*T, len(matrix_sequence_encoding[i]))
		yf = fft(matrix_sequence_encoding[i])
		xf = np.linspace(0.0, 1.0/(2.0*T), len(matrix_sequence_encoding[i])//2)
		matrix_digitized.append(np.abs(yf[0:len(matrix_sequence_encoding[i])//2]))

	header = ["P_"+str(i+1) for i in range(len(matrix_digitized[0]))]
	dataset_export = pd.DataFrame(matrix_digitized, columns=header)
	dataset_export["response"] = dataset['inhibition_IC50']
		


	

