import pandas as pd
import sys
import plotly.express as px

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]
list_domains = list(set(dataset['domains']))

count_domain = []

for domain in list_domains:
	cont=0
	for i in range(len(dataset)):
		if dataset['domains'][i] == domain:
			cont+=1

	count_domain.append(cont)

print("Create graph")
dataframe = pd.DataFrame()
dataframe['value'] = count_domain
dataframe['domain'] = list_domains

fig = px.pie(dataframe, values='value', names='domain', title='Domain preference by peptides')
fig.write_image(path_output+"4_summary_preference_domain.svg")

print("Export data")
dataframe.to_csv(path_output+"4_summary_preference_domain.csv", index=False)
