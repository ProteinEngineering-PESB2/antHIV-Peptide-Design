import pandas as pd
import sys
import plotly.graph_objects as go

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

family_split = list(set(dataset['domain']))

fig = go.Figure()

#for each data apply a count to get values per classification
for family in family_split:

	print("Process domain: ", family)
	cont_c1 = 0
	cont_c2 = 0
	cont_c3 = 0

	for i in range(len(dataset)):
		if dataset['domain'][i] == family:
			if dataset['categorized_IC50'][i] == "Class I":
				cont_c1+=1
			elif dataset['categorized_IC50'][i] == "Class II":
				cont_c2+=1
			else:
				cont_c3+=1

	array_categories = [cont_c1, cont_c2, cont_c3]
	print(array_categories)
	fig.add_trace(go.Bar(
	    x=["Class I", "Class II", "Class III"],
	    y=array_categories,
	    name=family
	))

fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.write_image(path_output+"5_summary_counts_domain_per_class.svg")
