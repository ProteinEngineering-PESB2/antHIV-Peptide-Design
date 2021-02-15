import pandas as pd
import sys
import numpy as np

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]
domain_analysis = sys.argv[3]

for class_data in ["Class I", "Class II", "Class III"]:
	try:
		print("Process statistic by class: ", class_data)

		matrix_subset = []

		for i in range(len(dataset)):
			if dataset['domain'][i] == domain_analysis:
				if dataset['categorized_IC50'][i] == class_data:
					row = [dataset[key][i] for key in dataset.keys()]
					matrix_subset.append(row)

		dataset_subclass = pd.DataFrame(matrix_subset, columns=dataset.keys())
		matrix_data_statistical = []

		for feature in ['length','molecular_weigth','charge','charge_density','isoelectric','inestability','aromaticity','aliphatic_index','hydrophobic_ratio','hydrophobicity_profile','hydrophobic_profile','inhibition_IC50']:

			print("Process feature: ", feature)

			min_value = np.min(dataset_subclass[feature])
			max_value = np.max(dataset_subclass[feature])
			avg_value = np.mean(dataset_subclass[feature])
			std_value = np.std(dataset_subclass[feature])
			q1_value = np.quantile(dataset_subclass[feature], .25)
			q3_value = np.quantile(dataset_subclass[feature], .75)

			row = [min_value, max_value, avg_value, std_value, q1_value, q3_value]
			matrix_data_statistical.append(row)

		print("Export statistical summary")
		dataset_statistical = pd.DataFrame(matrix_data_statistical, columns = ["min_value", "max_value", "avg_value", "std_value", "q1_value", "q3_value"])
		dataset_statistical["feature"] = ['length','molecular_weigth','charge','charge_density','isoelectric','inestability','aromaticity','aliphatic_index','hydrophobic_ratio','hydrophobicity_profile','hydrophobic_profile','inhibition_IC50']
		dataset_statistical.to_csv(path_output+class_data+"_statistical_summary.csv", index=False)
	except:
		pass