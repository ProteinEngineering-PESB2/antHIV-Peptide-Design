import pandas as pd
import sys
import matplotlib.pyplot as plt

def read_matrix_digitized(name_file):

	matrix_data = []
	file_data = open(name_file, 'r')
	line = file_data.readline()

	while line:

		row = line.replace("\n", "").split(",")
		row = [float(value) for value in row]
		matrix_data.append(row)
		line = file_data.readline()

	file_data.close()

	return matrix_data

def search_sequences(index_sequences, sequences):

	index_array = []

	for sequence in sequences:
		for i in range(len(index_sequences)):
			if index_sequences['sequence'][i] == sequence:
				index_array.append(i)
				break

	return index_array

def make_graph_representation(domain_values, matrix_values, property_data, output):

	plt.clf()
	#make figure
	for i in range(len(matrix_values)):

		plt.plot(domain_values, matrix_values[i])	
	plt.xlabel('Points')
	plt.ylabel('Values in points')
	plt.title(property_data)
	plt.savefig(output)
	plt.clf()


dataset = pd.read_csv(sys.argv[1])
path_digitized = sys.argv[2]
path_output = sys.argv[3]

unique_domains = list(set(dataset['domain']))

#get sequences by domain
for domain in unique_domains:
	print("Process domain ", domain)
	sequences = []

	for i in range(len(dataset)):
		if dataset['domain'][i] == domain:
			sequences.append(dataset['sequence'][i])

	for prop in ["alpha-structure_group", "betha-structure_group", "energetic_group", "hydropathy_group", "hydrophobicity_group", "index_group", "secondary_structure_properties_group", "volume_group"]:

		print("Process property: ", prop)
		index_sequences = pd.read_csv(path_digitized+prop+"/index_sequences.csv")
		matrix_for_property = read_matrix_digitized(path_digitized+prop+"/encoding_data_FFT.csv")
		domain_frequency = read_matrix_digitized(path_digitized+prop+"/domain_data.csv")

		#search sequences into matrix based on index and get values for make graph
		values_property = [matrix_for_property[index] for index in search_sequences(index_sequences, sequences)]

		#make graph
		name_output = path_output+domain+"/spectrum_for_property_"+prop+".svg"
		make_graph_representation(domain_frequency[0], values_property, prop, name_output)
	