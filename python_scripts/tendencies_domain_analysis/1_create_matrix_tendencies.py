import pandas as pd
import sys

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

#update counts
for i in range(len(dataset)):
	
	for key in ['Align with loop1', 'Align with PBD','Align with CHR','Align with LPB','Align with loop2']:
		dataset[key][i] =0

#update data counts using domain preferences
for i in range(len(dataset)):

	print("Process sequence: ", i)
	
	#evaluate not division
	if dataset['Not_division'][i] == "chr_domain":
		dataset['Align with PBD'][i]+=1
		dataset['Align with CHR'][i]+=1
		dataset['Align with LPB'][i]+=1

	#evaluated two division
	if dataset['two_domains'][i] == "loop1_PBD":
		dataset['Align with loop1'][i]+=1
		dataset['Align with PBD'][i]+=1 	

	if dataset['two_domains'][i] == "PBD_CHR":
		dataset['Align with PBD'][i]+=1
		dataset['Align with CHR'][i]+=1

	if dataset['two_domains'][i] == "CHR_LPB":
		dataset['Align with CHR'][i]+=1
		dataset['Align with LPB'][i]+=1


	#evaluated three division
	if dataset['three_domains'][i] == "CHR_LPB_loop2":
		dataset['Align with CHR'][i]+=1
		dataset['Align with LPB'][i]+=1
		dataset['Align with loop2'][i]+=1	

	if dataset['three_domains'][i] == "loop1_PBD_CHR":
		dataset['Align with CHR'][i]+=1
		dataset['Align with PBD'][i]+=1
		dataset['Align with loop1'][i]+=1

	#evaluated four division
	if dataset['four_domains'][i] == "PBD_CHR_LPB_loop2":
		dataset['Align with CHR'][i]+=1
		dataset['Align with PBD'][i]+=1
		dataset['Align with LPB'][i]+=1
		dataset['Align with loop2'][i]+=1

	if dataset['four_domains'][i] == "loop1_PBD_CHR_LPB":
		dataset['Align with CHR'][i]+=1
		dataset['Align with PBD'][i]+=1
		dataset['Align with LPB'][i]+=1
		dataset['Align with loop1'][i]+=1

	#evaluated full domain with loops
	if dataset['full_join_data'][i] == "loop1_PBD_CHR_LPB_loop2":
		dataset['Align with CHR'][i]+=1
		dataset['Align with PBD'][i]+=1
		dataset['Align with LPB'][i]+=1
		dataset['Align with loop1'][i]+=1
		dataset['Align with loop2'][i]+=1

dataset.to_csv(path_output+"2_update_count_tendencies.csv", index=False)