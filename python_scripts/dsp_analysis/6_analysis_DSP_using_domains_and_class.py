import pandas as pd
import sys
import os
from scipy.fft import fft
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def process_dsp_analysis(sequence, domain, path_encoding, path_output, T, xf):

	#make encoding data
	list_clusters = ["alpha-structure_group", "betha-structure_group", "energetic_group", "hydropathy_group", "hydrophobicity_group", "index_group", "secondary_structure_properties_group", "volume_group"]

	for cluster in list_clusters:

		dataset_cluster = pd.read_csv(path_encoding+"encoding_AAIndex/"+cluster+"/data_component.csv")

		matrix_sequence_encoding = []

		sequence_encoding = encoding_sequence(sequence, dataset_cluster['component_1'])		
		matrix_sequence_encoding.append(sequence_encoding)

		#make zero padding	
		for i in range(len(matrix_sequence_encoding)):
			for j in range(len(matrix_sequence_encoding[i]),64):
				matrix_sequence_encoding[i].append(0)

		print("Export encoding sequence")
		dataset_encoding = pd.DataFrame(matrix_sequence_encoding)
		dataset_encoding.to_csv(path_output+cluster+"/"+ domain+"_sequence_encoding.csv", index=False, header=False)

		print("Encoding using fft Python")

		matrix_digitized = []

		for i in range(len(matrix_sequence_encoding)):
			
			x = np.linspace(0.0, len(matrix_sequence_encoding[i])*T, len(matrix_sequence_encoding[i]))
			yf = fft(matrix_sequence_encoding[i])
			matrix_digitized.append(np.abs(yf[0:len(matrix_sequence_encoding[i])//2]))

		header = ["P_"+str(i+1) for i in range(len(matrix_digitized[0]))]
		dataset_export = pd.DataFrame(matrix_digitized, columns=header)

		dataset_export.to_csv(path_output+cluster+"/"+domain+"_sequence_digitized_using_python.csv", index=False, header=False)


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

#define sequences and domain data
sequence = "AVGIGALFLGFLGAAGSTMGAASMTLTVQARQLLSGIVQQQNNLLRAIEAQQHLLQLTVWGIKQLQARILAVERYLKDQQLLGIWGCSGKLICTTAVPWNASWSNKSLEQIWNHTTWMEWDREINNYTSLIHSLIEESQNQQEKNEQELLELDKWASLWNWFNITNWLWYIKLFIMIVGGLVGLRIVFAVLSIVNRVRQGYSPLSFQTHLPTPRGPDRPEGIEEEGGERDRDRSIRLVNGSLALIWDDLRSLCLFSYHRLRDLLLIVTRIVELLGRRGWEALKYWWNLLQYWSQELKNSAVSLLNATAIAVAEGTDRVIEVVQGACRAIRHIPRRIRQGLERILL"
pbd_chr_domain = sequence[116:155]
chr_domain = sequence[116:162]
chr_lpb_domain = sequence[124:162]

dataset = pd.read_csv(sys.argv[1])
path_input = sys.argv[2]
path_encoding = sys.argv[3]

list_clusters = ["alpha-structure_group", "betha-structure_group", "energetic_group", "hydropathy_group", "hydrophobicity_group", "index_group", "secondary_structure_properties_group", "volume_group"]

color_data_fill = ['rgba(0,100,80,0.2)', 'rgba(0,176,246,0.2)', 'rgba(231,107,243,0.2)']
color_data_figure = ['rgb(0,100,80)', 'rgb(0,176,246)', 'rgb(231,107,243)']

T = 1.0/float(64)
xf = np.linspace(0.0, 1.0/(2.0*T), 64//2)
