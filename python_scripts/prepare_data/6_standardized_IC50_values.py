import pandas as pd
import sys

def get_new_status_value(unity, value_inhibition, mw):
	
	new_value = None

	if unity == "mg/mL":
		new_value = value_inhibition*1000000000/mw
	
	if unity == "ng/ml":
		new_value = value_inhibition*1000/mw

	if unity == "uM":
		new_value = value_inhibition*1000

	if unity == "nM":
		new_value = value_inhibition

	if unity == "ug/ml":
		new_value = value_inhibition*1000000/mw

	return new_value

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

#remove standar deviation
for i in range(len(dataset)):

	if "+" in  str(dataset['inhibition_IC50'][i]):
		value = dataset['inhibition_IC50'][i].split("+")[0]
		dataset['inhibition_IC50'][i] = value

#update data change float status
for i in range(len(dataset)):
	if str(dataset['inhibition_IC50'][i]) != "nan":
		dataset['inhibition_IC50'][i] = float(dataset['inhibition_IC50'][i])

unity_values = list(set(dataset['inhibition_unit']))

unity_values = [value for value in unity_values if str(value) != "nan"]

for i in range(len(dataset)):
	print("Process sequence: ", dataset['sequence'][i])
	new_value = get_new_status_value(dataset['inhibition_unit'][i], dataset['inhibition_IC50'][i], dataset['molecular_weigth'][i] )
	
	dataset['inhibition_IC50'][i] = new_value
	dataset['inhibition_unit'][i] = "nM"
	
dataset.to_csv(path_output+"6_correct_IC50.csv", index=False)
