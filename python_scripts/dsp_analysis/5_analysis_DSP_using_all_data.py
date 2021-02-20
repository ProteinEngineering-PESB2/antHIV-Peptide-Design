import pandas as pd
import sys
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

path_input = sys.argv[1]
data_categories = pd.read_csv(sys.argv[2])

list_clusters = ["alpha-structure_group", "betha-structure_group", "energetic_group", "hydropathy_group", "hydrophobicity_group", "index_group", "secondary_structure_properties_group", "volume_group"]

color_data_fill = ['rgba(0,100,80,0.2)', 'rgba(0,176,246,0.2)', 'rgba(231,107,243,0.2)']
color_data_figure = ['rgb(0,100,80)', 'rgb(0,176,246)', 'rgb(231,107,243)']

T = 1.0/float(512)
xf = np.linspace(0.0, 1.0/(2.0*T), 512//2)

for cluster in list_clusters:

	print("Process cluster: ", cluster)

	data_cluster = pd.read_csv(path_input+cluster+"/encoding_data_multiplicacion.csv")

	data_merged = pd.merge(data_cluster, data_categories, on="sequence")

	print("Process data by class and get information")

	index=0
	fig = go.Figure()
	for class_data in ["Class I", "Class II", "Class III"]:

		print("Process data class: ", class_data)
		matrix_values = []

		for i in range(len(data_merged)):
			if data_merged['categorized_IC50'][i] == class_data:
				row = [data_merged[key][i] for key in data_merged.keys() if key[0] == "P" and key[1]=="_"]
				matrix_values.append(row)

		header = [key for key in data_merged.keys() if key[0] == "P" and key[1]=="_"]

		dataset_export_figure = pd.DataFrame(matrix_values, columns=header)

		curve_average = []
		curve_max = []
		curve_min = []
		curve_q1 = []
		curve_q3 = []

		for key in dataset_export_figure.keys():
			curve_average.append(np.mean(dataset_export_figure[key]))
			curve_min.append(np.min(dataset_export_figure[key]))
			curve_max.append(np.max(dataset_export_figure[key]))
			curve_q1.append(np.quantile(dataset_export_figure[key], .25))
			curve_q1.append(np.quantile(dataset_export_figure[key], .75))
			
		fig.add_trace(go.Scatter(x=xf, y=curve_average, name="Average "+ class_data, line_shape='spline', line_color=color_data_figure[index]))

		index+=1

	fig.update_traces(mode='lines')

	fig.update_layout(title='Average curve comparisson: '+cluster,
                   xaxis_title='Domain',
                   yaxis_title='Frequency')

	fig.write_image(path_input+cluster+"/summary_curves_compare.svg")
