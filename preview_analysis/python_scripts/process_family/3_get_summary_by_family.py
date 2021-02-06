import pandas as pd
import sys
import matplotlib.pyplot as plt


dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

unique_domain = list(set(dataset['domain']))

count_array = []

for i in range(len(unique_domain)):
	cont=0

	for domain in dataset['domain']:
		if domain == unique_domain[i]:
			cont+=1

	count_array.append(cont)

#make piechart
fig1, ax1 = plt.subplots()
ax1.pie(count_array, labels=unique_domain, autopct='%1.1f%%', shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.savefig(path_output+"summary_counts_domains.svg")

dataExport = pd.DataFrame()
dataExport['domain'] = unique_domain
dataExport['counts'] = count_array

dataExport.to_csv(path_output+"summary_counts_domain.csv", index=False)
