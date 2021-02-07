#!/usr/bin/env python

import pandas as pd
import sys

print("Read data")
data_JAH = pd.read_csv(sys.argv[1])
data_db = pd.read_excel(sys.argv[2], sheet_name="Sheet1")
path_output = sys.argv[3]

print("Get unique sequences data by dataset")
unique_sequences_JAH = list(set(data_JAH['sequence']))
unique_sequences_DB = list(set(data_db['SEQUENCE']))

sequences_data_merge = []

for sequence in unique_sequences_JAH:
	if sequence in unique_sequences_DB:
		sequences_data_merge.append(sequence)

print(len(sequences_data_merge))

print("Export repeat sequences")
dataset = pd.DataFrame(sequences_data_merge, columns=["sequence"])
dataset.to_csv(path_output+"1_merge_seques.csv", index=False)

print("Process unique sequences")
unique_sequences = unique_sequences_DB+unique_sequences_JAH
unique_sequences = list(set(unique_sequences))
print(len(unique_sequences))
dataset = pd.DataFrame(unique_sequences, columns=["sequence"])
dataset.to_csv(path_output+"1_unique_sequences.csv", index=False)
