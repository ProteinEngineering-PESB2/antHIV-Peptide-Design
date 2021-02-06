#!/usr/bin/env python

import pandas as pd
import sys

data_JAH = pd.read_csv(sys.argv[1])
data_db = pd.read_excel(sys.argv[2], sheet_name="Sheet1")
path_output = sys.argv[3]

unique_sequences_JAH = list(set(data_JAH['sequence']))
unique_sequences_DB = list(set(data_db['SEQUENCE']))

sequences_data_merge = []

for sequence in unique_sequences_JAH:
	if sequence in unique_sequences_DB:
		sequences_data_merge.append(sequence)

print(len(sequences_data_merge))

dataset = pd.DataFrame(sequences_data_merge, columns=["sequence"])
dataset.to_csv(path_output+"merge_seques.csv", index=False)