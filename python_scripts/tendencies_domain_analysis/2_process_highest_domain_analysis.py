import pandas as pd
import sys

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

keys = ['Align with loop1', 'Align with PBD','Align with CHR','Align with LPB','Align with loop2']

tendencies = []

for i in range(len(dataset)):

	row_values = [dataset[key][i] for key in keys]
	max_value = max(row_values)

	if max_value>0:
		tendency_example = ""

		for key in keys:
			if dataset[key][i] >= max_value:
				tendency_example = tendency_example+ key + ";"

		tendency_example = tendency_example.replace("Align with ", "")
		if tendency_example[-1] == ";":
			tendency_example = tendency_example[:-1]

		tendency_example = tendency_example.replace(";", "-")
		
		row_value = [dataset['sequence'][i], tendency_example, max_value]
		tendencies.append(row_value)
	else:
		row_value = [dataset['sequence'][i], "Non-tendency", 0]
		tendencies.append(row_value)

print("Export tendencies data")
tendencies = pd.DataFrame(tendencies, columns=["sequence", "domains", "number_values"])
tendencies.to_csv(path_output+"3_get_tendencies_by_peptide.csv", index=False)

