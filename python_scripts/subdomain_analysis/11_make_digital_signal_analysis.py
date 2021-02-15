import pandas as pd
import sys
from scipy.fft import fft
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

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

dataset_input = pd.read_csv(sys.argv[1])

domain_to_evaluate = sys.argv[4]

#process dataset, selecting the features concerning the domain to evaluate
matrix_data = []

for i in range(len(dataset_input)):
	if dataset_input['domain'][i] == domain_to_evaluate:
		row = [dataset_input[key][i] for key in dataset_input.keys()]
		matrix_data.append(row)

dataset = pd.DataFrame(matrix_data, columns=dataset_input.keys())

path_output = sys.argv[2]
path_encoding = sys.argv[3]

list_clusters = ["alpha-structure_group", "betha-structure_group", "energetic_group", "hydropathy_group", "hydrophobicity_group", "index_group", "secondary_structure_properties_group", "volume_group"]

color_data_fill = ['rgba(0,100,80,0.2)', 'rgba(0,176,246,0.2)', 'rgba(231,107,243,0.2)']
color_data_figure = ['rgb(0,100,80)', 'rgb(0,176,246)', 'rgb(231,107,243)']

for cluster in list_clusters:

	print("Process property: ", cluster)

	dataset_cluster = pd.read_csv(path_encoding+"encoding_AAIndex/"+cluster+"/data_component.csv")

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
		for j in range(len(matrix_sequence_encoding[i]),1024):
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
	dataset_export["response"] = dataset['categorized_IC50']
	dataset_export["id_sequence"] = dataset['id_sequence']

	dataset_export.to_csv(path_output+cluster+"_encoding_data.csv", index=False)
	print("Create line chart")
	matrix_data = []

	for i in range(len(dataset_export)):

		index=0
		for key in dataset_export.keys():
			if key not in ["response", "id_sequence"]:
				row = [dataset_export['id_sequence'][i], dataset_export['response'][i], xf[index], dataset_export[key][i]]
				index+=1
				matrix_data.append(row)
	
	dataset_figure = pd.DataFrame(matrix_data, columns=["id_sequence", "categorized_IC50", "domain", "frequency"])	

	fig = px.line(dataset_figure, x="domain", y="frequency", color="categorized_IC50", line_group="id_sequence", hover_name="id_sequence")
	fig.write_image(path_output+cluster+".svg")

	#estimated average curves per class
	statistical_curves = {}

	print("Process statistical curves for property: ", cluster)
	fig = go.Figure()

	print(list(set(dataset_export['response'])))

	index=0
	for class_data in ["Class I", "Class II", "Class III"]:

		try:
			print("Process data class: ", class_data)
			matrix_values = []

			for i in range(len(dataset_export)):
				if dataset_export['response'][i] == class_data:
					row = [dataset_export[key][i] for key in dataset_export.keys()]
					matrix_values.append(row)

			dataset_export_figure = pd.DataFrame(matrix_values, columns=dataset_export.keys())

			curve_average = []
			curve_max = []
			curve_min = []
			curve_q1 = []
			curve_q3 = []

			for key in dataset_export_figure.keys():
				if key not in ["response", "id_sequence"]:

					curve_average.append(np.mean(dataset_export_figure[key]))
					curve_min.append(np.min(dataset_export_figure[key]))
					curve_max.append(np.max(dataset_export_figure[key]))
					curve_q1.append(np.quantile(dataset_export_figure[key], .25))
					curve_q1.append(np.quantile(dataset_export_figure[key], .75))
			
			fig.add_trace(go.Scatter(x=xf, y=curve_average, name="Average "+ class_data,
	                    line_shape='spline', line_color=color_data_figure[index]))
		except:
			pass
		index+=1
		
	fig.update_traces(mode='lines')

	fig.update_layout(title='Average curve: '+cluster,
                   xaxis_title='Domain',
                   yaxis_title='Frequency')

	fig.write_image(path_output+cluster+"summary_curves.svg")
