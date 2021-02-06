import pandas as pd
import sys

def search_ic50_value_DB(dataset, sequence, key):

	index = -1
	
	for i in range(len(dataset)):
		if dataset[key][i] == sequence:
			index=i
			break

	return index

dataset = pd.read_csv(sys.argv[1])
database_JAH = pd.read_csv(sys.argv[2])
database_HIV = pd.read_excel(sys.argv[3], sheet_name="Sheet1")
path_output = sys.argv[4]

dataset['name_peptide'] = ['' for i in range(len(dataset))]
dataset['source'] = ['' for i in range(len(dataset))]
dataset['host'] = ['' for i in range(len(dataset))]
dataset['assay'] = ['' for i in range(len(dataset))]
dataset['PMID/DOI'] = ['' for i in range(len(dataset))]

for i in range(len(dataset)):

	#search in JAH database
	print("Process sequence: ", dataset['sequence'][i])

	#search sequence in DB JAH
	index = search_ic50_value_DB(database_JAH, dataset['sequence'][i], 'sequence')
	
	if index != -1:
		dataset['name_peptide'][i] = database_JAH['name'][index]
		dataset['host'][i] = database_JAH['IC_50_enter_host'][index]
	else:
		index = search_ic50_value_DB(database_HIV, dataset['sequence'][i], 'SEQUENCE')
		
		dataset['name_peptide'][i] = database_HIV['NOMENCLATURE'][index]
		dataset['source'][i] = database_HIV['SOURCE'][index]
		dataset['host'][i] = database_HIV['CELL LINE'][index]
		dataset['assay'][i] = database_HIV['ASSAY'][index]
		dataset['PMID/DOI'][i] = database_HIV['PMID'][index]

dataset.to_csv(path_output+"dataset_all_features.csv", index=False)

