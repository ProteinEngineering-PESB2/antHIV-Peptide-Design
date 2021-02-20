import pandas as pd
import sys
import plotly.express as px

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

class_unique = list(set(dataset['categorized_IC50']))

count_array = []
domain_array = []

print("Make counts data")
for i in range(len(class_unique)):
	cont=0

	for domain in dataset['categorized_IC50']:
		if domain == class_unique[i]:
			cont+=1

	count_array.append(cont)
	domain_array.append(class_unique[i])

print("Create graph")
dataframe = pd.DataFrame()
dataframe['value'] = count_array
dataframe['class'] = domain_array

fig = px.pie(dataframe, values='value', names='class', title='Class distribution by peptides')
fig.write_image(path_output+"10_summary_counts_category.png")

print("Export data")
dataframe.to_csv(path_output+"10_summary_counts_category.csv", index=False)
