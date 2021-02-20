import pandas as pd
import sys
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
path_encoding = sys.argv[2]
path_output = sys.argv[3]

list_clusters = ["alphaStructureGroup", "bethaStructureGroup", "energeticGroup", "hydropathyGroup", "hydrophobicityGroup", "indexGroup", "secondaryStructurePropertiesGroup", "volumeGroup"]
sequence = "AVGIGALFLGFLGAAGSTMGAASMTLTVQARQLLSGIVQQQNNLLRAIEAQQHLLQLTVWGIKQLQARILAVERYLKDQQLLGIWGCSGKLICTTAVPWNASWSNKSLEQIWNHTTWMEWDREINNYTSLIHSLIEESQNQQEKNEQELLELDKWASLWNWFNITNWLWYIKLFIMIVGGLVGLRIVFAVLSIVNRVRQGYSPLSFQTHLPTPRGPDRPEGIEEEGGERDRDRSIRLVNGSLALIWDDLRSLCLFSYHRLRDLLLIVTRIVELLGRRGWEALKYWWNLLQYWSQELKNSAVSLLNATAIAVAEGTDRVIEVVQGACRAIRHIPRRIRQGLERILL"

length_sequences = [len(sequence) for sequence in dataset['sequence']]

for cluster in list_clusters:

	print(cluster)

	dataset_cluster = pd.read_csv(path_encoding+cluster+".csv")

	matrix_sequence_encoding = []
	class_data = []
	predict_data = []

	protein_encoding = encoding_sequence(sequence, dataset_cluster['component_1'])

	for i in range(len(protein_encoding), 512):
		protein_encoding.append(0)

	yf_protein = fft(protein_encoding)

	for i in range(len(dataset)):

		sequence_encoding = encoding_sequence(dataset['sequence'][i], dataset_cluster['component_1'])		
		matrix_sequence_encoding.append(sequence_encoding)
		class_data.append(dataset['categorized_IC50'][i])
		predict_data.append(dataset['inhibition_IC50'][i])

	#make zero padding	
	for i in range(len(matrix_sequence_encoding)):
		for j in range(len(matrix_sequence_encoding[i]),512):
			matrix_sequence_encoding[i].append(0)

	print("Encoding using fft Python")

	matrix_digitized = []

	for i in range(len(matrix_sequence_encoding)):

		yf = fft(matrix_sequence_encoding[i])
		yf = yf*protein_encoding
		
		matrix_digitized.append(np.abs(yf[0:512//2]))

	header = ["P_"+str(i+1) for i in range(len(matrix_digitized[0]))]
	dataset_export = pd.DataFrame(matrix_digitized, columns=header)
	dataset_export['response_IC50'] = predict_data
	dataset_export['category_IC50'] = class_data

	dataset_export.to_csv(path_output+cluster+"_encoding_sequences.csv", index=False)
