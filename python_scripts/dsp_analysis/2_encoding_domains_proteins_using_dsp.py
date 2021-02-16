import pandas as pd
import sys
import os
from scipy.fft import fft
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def process_dsp_analysis(sequence, domain):

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

			T = 1.0/float(len(matrix_sequence_encoding[i]))
			x = np.linspace(0.0, len(matrix_sequence_encoding[i])*T, len(matrix_sequence_encoding[i]))
			yf = fft(matrix_sequence_encoding[i])
			xf = np.linspace(0.0, 1.0/(2.0*T), len(matrix_sequence_encoding[i])//2)
			matrix_digitized.append(np.abs(yf[0:len(matrix_sequence_encoding[i])//2]))

		header = ["P_"+str(i+1) for i in range(len(matrix_digitized[0]))]
		dataset_export = pd.DataFrame(matrix_digitized, columns=header)

		dataset_export.to_csv(path_output+cluster+"/"+domain+"_sequence_digitized_using_python.csv", index=False, header=False)

		print("Make figure using encoding data")
		fig = go.Figure()
		fig.add_trace(go.Scatter(x=xf, y=matrix_digitized[0], name="Domain: "+domain, line_shape='spline', line_color='rgb(0,100,80)'))

		fig.update_traces(mode='lines')

		fig.update_layout(title="Domain "+ domain+" curve: "+cluster,
	                   xaxis_title='Domain',
	                   yaxis_title='Frequency')

		fig.write_image(path_output+cluster+"/"+ domain+"_summary_curves_using_python.svg")

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

#input data
path_encoding = sys.argv[1]
path_output = sys.argv[2]

sequence = "AVGIGALFLGFLGAAGSTMGAASMTLTVQARQLLSGIVQQQNNLLRAIEAQQHLLQLTVWGIKQLQARILAVERYLKDQQLLGIWGCSGKLICTTAVPWNASWSNKSLEQIWNHTTWMEWDREINNYTSLIHSLIEESQNQQEKNEQELLELDKWASLWNWFNITNWLWYIKLFIMIVGGLVGLRIVFAVLSIVNRVRQGYSPLSFQTHLPTPRGPDRPEGIEEEGGERDRDRSIRLVNGSLALIWDDLRSLCLFSYHRLRDLLLIVTRIVELLGRRGWEALKYWWNLLQYWSQELKNSAVSLLNATAIAVAEGTDRVIEVVQGACRAIRHIPRRIRQGLERILL"

#only will be analysis the CHR  domain and sub domains

pbd_chr_domain = sequence[116:155]
chr_domain = sequence[116:162]
chr_lpb_domain = sequence[124:162]

print("Process domain PBD-CHR")
process_dsp_analysis(pbd_chr_domain, "PBD-CHR")

print("Process domain CHR full domain")
process_dsp_analysis(chr_domain, "CHR-full")

print("Process domain CHR-LPB")
process_dsp_analysis(chr_lpb_domain, "CHR-LPB")
