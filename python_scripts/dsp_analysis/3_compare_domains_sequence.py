import sys
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

path_input = sys.argv[1]
name_domains = ["PBD-CHR", "CHR-full", "CHR-LPB"]

list_clusters = ["alpha-structure_group", "betha-structure_group", "energetic_group", "hydropathy_group", "hydrophobicity_group", "index_group", "secondary_structure_properties_group", "volume_group"]
color_data_figure = ['rgb(0,100,80)', 'rgb(0,176,246)', 'rgb(231,107,243)']

for cluster in list_clusters:

	print("Process curves for cluster: ", cluster)
	fig = go.Figure()

	index=0
	for domain in name_domains:

		file_data = open(path_input+cluster+"/"+domain+"_sequence_digitized_using_python.csv", 'r')

		line_data = file_data.readline()
		file_data.close()

		row_values = line_data.replace("\n", "").split(",")
		row_values = [float(value) for value in row_values]

		T = 1.0/float(64)
		xf = np.linspace(0.0, 1.0/(2.0*T), 64//2)

		fig.add_trace(go.Scatter(x=xf, y=row_values, name=domain, line_shape='spline', line_color=color_data_figure[index]))
		index+=1

	fig.update_traces(mode='lines')

	fig.update_layout(title='Comparison domains curves for : '+cluster,
                   xaxis_title='Domain',
                   yaxis_title='Frequency')

	fig.write_image(path_input+cluster+"/summary_comparisson_curves.svg")