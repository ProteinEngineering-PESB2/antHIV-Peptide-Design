import sys
import os

path_input = sys.argv[1]
path_output = sys.argv[2]

list_clusters = ["alphaStructureGroup", "bethaStructureGroup", "energeticGroup", "hydropathyGroup", "hydrophobicityGroup", "indexGroup", "secondaryStructurePropertiesGroup", "volumeGroup"]

for cluster in list_clusters:

	command = "mkdir -p "+ path_output+cluster
	print(command)
	os.system(command)

	command = "python3 training_classification_models.py %s%s_encoding_sequences.csv %s%s/" % (path_input, cluster, path_output, cluster)
	print(command)
	os.system(command)


