import pandas as pd
import sys
import numpy as np
from scipy.fft import fft
import plotly.express as px
import plotly.graph_objects as go

def encoding_using_fft_values(sequence_encoding):

	T = 1.0/float(512)
	x = np.linspace(0.0, 512*T, 512)
	yf = fft(sequence_encoding)
	xf = np.linspace(0.0, 1.0/(2.0*T), 512//2)
	yf_abs = np.abs(yf[0:512//2])

	return yf, yf_abs

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

	length_value = len(sequence_encoding)
	for i in range(length_value, 512):
		sequence_encoding.append(0)

	return sequence_encoding

sequence = "AVGIGALFLGFLGAAGSTMGAASMTLTVQARQLLSGIVQQQNNLLRAIEAQQHLLQLTVWGIKQLQARILAVERYLKDQQLLGIWGCSGKLICTTAVPWNASWSNKSLEQIWNHTTWMEWDREINNYTSLIHSLIEESQNQQEKNEQELLELDKWASLWNWFNITNWLWYIKLFIMIVGGLVGLRIVFAVLSIVNRVRQGYSPLSFQTHLPTPRGPDRPEGIEEEGGERDRDRSIRLVNGSLALIWDDLRSLCLFSYHRLRDLLLIVTRIVELLGRRGWEALKYWWNLLQYWSQELKNSAVSLLNATAIAVAEGTDRVIEVVQGACRAIRHIPRRIRQGLERILL"

dataset_peptides = pd.read_csv(sys.argv[1])
path_encoding = sys.argv[2]
path_output = sys.argv[3]

list_clusters = ["alpha-structure_group", "betha-structure_group", "energetic_group", "hydropathy_group", "hydrophobicity_group", "index_group", "secondary_structure_properties_group", "volume_group"]

for cluster in list_clusters:

	print("Process cluster: ", cluster)

	dataset_cluster = pd.read_csv(path_encoding+"encoding_AAIndex/"+cluster+"/data_component.csv")

	matrix_sequence_encoding = []

	print("Process sequence GP41")

	gp41_sequence_encoding = encoding_sequence(sequence, dataset_cluster['component_1'])	
	yf_gp41, yf_abs_gp41 = encoding_using_fft_values(gp41_sequence_encoding)

	print("Process sequences")
	matrix_encoding = []
	for i in range(len(dataset_peptides)):

		sequence_encoding = encoding_sequence(dataset_peptides['sequence'][i], dataset_cluster['component_1'])
		yf_sequence, yf_abs_sequence = encoding_using_fft_values(sequence_encoding)

		result = yf_sequence*yf_gp41

		yf_abs = np.abs(result[0:512//2])

		row = [dataset_peptides['sequence'][i]]

		for value in yf_abs:
			row.append(value)

		matrix_encoding.append(row)

	header = ["sequence"]

	for i in range(len(matrix_encoding[0])-1):
		header.append("P_"+str(i+1))

	print("Export data")
	dataset_export = pd.DataFrame(matrix_encoding, columns=header)
	dataset_export.to_csv(path_output+cluster+"/encoding_data_multiplicacion.csv", index=False)
