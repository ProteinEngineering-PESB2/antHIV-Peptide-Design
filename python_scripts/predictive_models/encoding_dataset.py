import pandas as pd
import sys
import numpy as np
import torch
from tape import ProteinBertModel, TAPETokenizer

def encoding_sequence_using_frequency(sequence):

	array_residues = ['A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
	
	encoding_sequence = []

	for residue in sequence:

		cont=0
		for residue2 in sequence:
			if residue2 == residue:
				cont+=1

		cont = float(cont)/float(len(sequence))
		encoding_sequence.append(cont)

	return encoding_sequence

def encoding_sequence_using_onehot(sequence):

	array_residues = ['A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
	encoding_sequence = []

	for residue in sequence:

		encoding_residue = [0 for value in array_residues]

		for i in range(len(array_residues)):
			if array_residues[i] == residue:
				encoding_residue[i] = 1
				break

		for value in encoding_residue:
			encoding_sequence.append(value)

	return encoding_sequence

def encoding_sequence_using_ordinal(sequence):
	
	array_residues = ['A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
	encoding_sequence = []

	for residue in sequence:

		for i in range(len(array_residues)):
			if array_residues[i] == residue:
				encoding_sequence.append(i)
				break

	return encoding_sequence

def encoding_sequence_using_tape(sequence, model, tokenizer):
	

	try:
		array_residues = ['A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
		
		token_ids = torch.tensor([tokenizer.encode(sequence)])
		output = model(token_ids)
		sequence_output = output[0]
		
		matrix_data = []

		for element in sequence_output[0].cpu().detach().numpy():
			matrix_data.append(element)	

		encoding_avg = []

		for i in range(len(matrix_data[0])):
			array_value = []
			for j in range(len(matrix_data)):
				array_value.append(matrix_data[j][i])

			encoding_avg.append(np.mean(array_value))

		return encoding_avg

	except:
		return -1

model = ProteinBertModel.from_pretrained('bert-base')
tokenizer = TAPETokenizer(vocab='iupac')  # iupac is the vocab for TAPE models, use unirep for the UniRep model

dataset = pd.read_csv(sys.argv[1])
type_encoding = int(sys.argv[2])
name_output = sys.argv[3]

matrix_encoding_data = []
response_data_class = []
response_data_predi = []

length_sequences = []

print("Encoding sequence")
for i in range(len(dataset)):

	length_sequences.append(len(dataset['sequence'][i]))

	sequence_encoding = []

	if type_encoding == 1:
		sequence_encoding = encoding_sequence_using_ordinal(dataset['sequence'][i])
		response_data_predi.append(dataset['inhibition_IC50'][i])
		response_data_class.append(dataset['categorized_IC50'][i])
		matrix_encoding_data.append(sequence_encoding)
		
	elif type_encoding == 2:
		sequence_encoding = encoding_sequence_using_onehot(dataset['sequence'][i])
		response_data_class.append(dataset['categorized_IC50'][i])
		response_data_predi.append(dataset['inhibition_IC50'][i])
		matrix_encoding_data.append(sequence_encoding)

	elif type_encoding == 3:
		sequence_encoding = encoding_sequence_using_frequency(dataset['sequence'][i])
		response_data_predi.append(dataset['inhibition_IC50'][i])
		response_data_class.append(dataset['categorized_IC50'][i])
		matrix_encoding_data.append(sequence_encoding)

	else:
		sequence_encoding = encoding_sequence_using_tape(dataset['sequence'][i], model, tokenizer)

		if sequence_encoding != -1:
			response_data_class.append(dataset['categorized_IC50'][i])
			response_data_predi.append(dataset['inhibition_IC50'][i])
			matrix_encoding_data.append(sequence_encoding)

if type_encoding != 4:#apply zero padding
	
	if type_encoding == 1 or type_encoding == 3:
		print("Apply zero padding")
		for i in range(len(matrix_encoding_data)):
			for j in range(len(matrix_encoding_data[i]), max(length_sequences)):
				matrix_encoding_data[i].append(0)
	else:
		print("Apply zero padding one hot")
		lenth_matrix = [len(data) for data in matrix_encoding_data]

		for i in range(len(matrix_encoding_data)):
			for j in range(len(matrix_encoding_data[i]), max(lenth_matrix)):
				matrix_encoding_data[i].append(0)

#create dataset

print("Export dataset")
header = ["P_"+str(i+1) for i in range(len(matrix_encoding_data[0]))]

data_export = pd.DataFrame(matrix_encoding_data, columns=header)
data_export['response_IC50'] = response_data_predi
data_export['category_IC50'] = response_data_class

data_export.to_csv(name_output, index=False)
	
