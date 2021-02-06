import pandas as pd
import sys

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

#remove null values
dataset_clean = dataset.dropna()
dataset_clean = dataset_clean.reset_index(drop=True)

#process response, get only value
for i in range(len(dataset_clean)):
	dataset_clean['IC_response'][i] = dataset_clean['IC_response'][i].split("+")[0].split(" ")[0].replace(",", ".")

#export dataset
dataset_clean.to_csv(path_output+"dataset_clean.csv", index=False)

