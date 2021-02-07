import pandas as pd
import sys

def search_ic50_value_DB(dataset, sequence, key):

	index = -1
	
	for i in range(len(dataset)):
		if dataset[key][i] == sequence:
			index=i
			break

	return index

dataset_full = pd.read_csv(sys.argv[1])
database_JAH = pd.read_csv(sys.argv[2])
database_HIV = pd.read_excel(sys.argv[3], sheet_name="Sheet1")
path_output = sys.argv[4]

dataset_full['inhibition_IC50'] = [0 for i in range(len(dataset_full))]
dataset_full['inhibition_unit'] = ['' for i in range(len(dataset_full))]

#search JAH peptides and add 
for i in range(len(dataset_full)):
	print("Process sequence: ", dataset_full['sequence'][i])

	#search sequence in DB JAH
	index = search_ic50_value_DB(database_JAH, dataset_full['sequence'][i], 'sequence')
	if index != -1:
		dataset_full['inhibition_IC50'][i] = database_JAH['IC_50_enter_mean'][index]
		dataset_full['inhibition_unit'][i] = "nM"

	index = search_ic50_value_DB(database_HIV, dataset_full['sequence'][i], 'SEQUENCE')
	if index != -1:		
		dataset_full['inhibition_IC50'][i] = database_HIV['INHIBITION/IC50'][index]
		dataset_full['inhibition_unit'][i] = database_HIV['UNIT'][index]

#export data
dataset_full.to_csv(path_output+"5_data_set_sequences_add_IC50_values.csv", index=False)

