import pandas as pd
import sys
import plotly.graph_objects as go

dataset = pd.read_csv(sys.argv[1])
path_result = sys.argv[2]
class_data = int(sys.argv[3])

ranges=[]
range_categories = []
if class_data==1:

	ranges = ["0-2", "2-4", "4-6", "6-8", "8-10"]
	range_categories = ["r1", "r2", "r3", "r4", "r5"]

elif class_data == 2:

	ranges = ["10-30", "30-50", "50-70", "70-90", "90-100"]
	range_categories = ["r1", "r2", "r3", "r4", "r5"]

else:
	ranges = ["100-200", "200-300", "300-400", "400-500"]
	range_categories = ["r1", "r2", "r3", "r4"]

categorie_ranking = []

for i in range(len(dataset)):

	if class_data==1:
		if dataset['inhibition_IC50'][i]>8 and dataset['inhibition_IC50'][i]<=10:
			categorie_ranking.append("r5")
		elif dataset['inhibition_IC50'][i]>6 and dataset['inhibition_IC50'][i]<=8:
			categorie_ranking.append("r4")

		elif dataset['inhibition_IC50'][i]>=4 and dataset['inhibition_IC50'][i]<6:
			categorie_ranking.append("r3")

		elif dataset['inhibition_IC50'][i]>=2 and dataset['inhibition_IC50'][i]<4:
			categorie_ranking.append("r2")
		else:
			categorie_ranking.append("r1")

	elif class_data==2:
		if dataset['inhibition_IC50'][i]<30:
			categorie_ranking.append("r1")
		elif dataset['inhibition_IC50'][i]>=30 and dataset['inhibition_IC50'][i]<50:
			categorie_ranking.append("r2")

		elif dataset['inhibition_IC50'][i]>=50 and dataset['inhibition_IC50'][i]<70:
			categorie_ranking.append("r3")

		elif dataset['inhibition_IC50'][i]>=70 and dataset['inhibition_IC50'][i]<90:
			categorie_ranking.append("r4")
		else:
			categorie_ranking.append("r5")		

	else:
		if dataset['inhibition_IC50'][i]<200:
			categorie_ranking.append("r1")
		elif dataset['inhibition_IC50'][i]>=200 and dataset['inhibition_IC50'][i]<300:
			categorie_ranking.append("r2")

		elif dataset['inhibition_IC50'][i]>=300 and dataset['inhibition_IC50'][i]<400:
			categorie_ranking.append("r3")
		else:
			categorie_ranking.append("r4")

dataset['ranking_IC50'] = categorie_ranking
dataset.to_csv(path_result+"add_ranking_class_"+str(class_data)+".csv", index=False)

print(dataset)
print("Make graph evaluation")

fig = go.Figure()

unique_domains = list(set(dataset['domains']))

for domain in unique_domains:

	print("Process domain: ", domain)
	count_data = []

	for value in range_categories:
		cont=0

		for i in range(len(dataset)):
			if dataset['ranking_IC50'][i] == value and dataset['domains'][i] == domain:
				cont+=1

		count_data.append(cont)

	print(count_data)
	fig.add_trace(go.Bar(
	    x=range_categories,
	    y=count_data,
	    name=domain
	))

fig.update_layout(barmode='group', xaxis_tickangle=-45, title='Preferences by selected domain by peptides', xaxis_title='Ranking by IC50', yaxis_title='Count')
fig.write_image(path_result+"summary_ranking_per_data_class"+str(class_data)+".svg")

