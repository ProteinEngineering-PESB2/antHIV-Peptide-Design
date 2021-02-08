import pandas as pd
import sys
import plotly.express as px

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

unique_domain = list(set(dataset['domain']))

count_array = []
domain_array = []

print("Make counts data")
for i in range(len(unique_domain)):
	cont=0

	for domain in dataset['domain']:
		if domain == unique_domain[i]:
			cont+=1

	count_array.append(cont)
	domain_array.append(unique_domain[i])

print("Create graph")
dataframe = pd.DataFrame()
dataframe['value'] = count_array
dataframe['domain'] = domain_array

fig = px.pie(dataframe, values='value', names='domain', title='Domain distribution by peptides')
fig.write_image(path_output+"3_summary_counts_domain.svg")

print("Export data")
dataframe.to_csv(path_output+"3_summary_counts_domain.csv", index=False)
