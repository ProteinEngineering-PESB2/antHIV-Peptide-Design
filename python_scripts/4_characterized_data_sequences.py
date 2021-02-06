import pandas as pd
import sys
from modlamp.descriptors import PeptideDescriptor, GlobalDescriptor

database = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

#estimated length of sequences
array_length = []

for i in range(len(database)):
	array_length.append(len(database['sequence'][i]))

database['length'] = array_length

print("Estimate formula")

#get formula for each sequence
formula_array = []

for i in range(len(database)):

	try:
		desc = GlobalDescriptor([database['sequence'][i]])
		desc.formula(amide=True)
		for v in desc.descriptor:
			formula_array.append(v[0])
	except:
		formula_array.append('')

database['formula'] = formula_array

print("Estimate molecular_weigth")
#get MW for each sequence
molecular_weigth_array = []

for i in range(len(database)):
	try:
		desc = GlobalDescriptor([database['sequence'][i]])
		desc.calculate_MW(amide=True)
		molecular_weigth_array.append(desc.descriptor[0][0])
	except:
		molecular_weigth_array.append('')

database['molecular_weigth'] = molecular_weigth_array

print("Estimate charge")
#calculate charge for each sequence
charge_array = []

for i in range(len(database)):
	try:
		desc = GlobalDescriptor([database['sequence'][i]])
		desc.calculate_charge(ph=7, amide=True)
		charge_array.append(desc.descriptor[0][0])
	except:
		charge_array.append('')

database['charge'] = charge_array

print("Estimate charge_density")
#calculate charge density for each sequence
charge_density_array = []

for i in range(len(database)):
	try:
		desc = GlobalDescriptor([database['sequence'][i]])
		desc.charge_density(ph=7, amide=True)
		charge_density_array.append(desc.descriptor[0][0])
	except:
		charge_density_array.append('')

database['charge_density'] = charge_density_array

print("Estimate isoelectric")
#estimate isoelectric point
isoelectric_array = []

for i in range(len(database)):
	try:
		desc = GlobalDescriptor([database['sequence'][i]])
		desc.isoelectric_point()
		isoelectric_array.append(desc.descriptor[0][0])
	except:
		isoelectric_array.append('')

database['isoelectric'] = isoelectric_array

print("Estimate inestability")
#estimate inestability index
inestability_array = []

for i in range(len(database)):
	try:
		desc = GlobalDescriptor([database['sequence'][i]])
		desc.instability_index()
		inestability_array.append(desc.descriptor[0][0])
	except:
		inestability_array.append('')

database['inestability'] = inestability_array

print("Estimate aromaticity")
#estimate aromaticity
aromaticity_array = []
for i in range(len(database)):
	try:
		desc = GlobalDescriptor([database['sequence'][i]])
		desc.aromaticity()
		aromaticity_array.append(desc.descriptor[0][0])
	except:
		aromaticity_array.append('')

database['aromaticity'] = aromaticity_array

print("Estimate aliphatic_index")
#estimate aliphatic_index
aliphatic_array = []
for i in range(len(database)):
	try:
		desc = GlobalDescriptor([database['sequence'][i]])
		desc.aliphatic_index()
		aliphatic_array.append(desc.descriptor[0][0])
	except:
		aliphatic_array.append('')

database['aliphatic_index'] = aliphatic_array

print("Estimate hydrophobic_ratio_array")
#estimate hydrophobic_ratio
hydrophobic_ratio_array = []
for i in range(len(database)):
	try:
		desc = GlobalDescriptor([database['sequence'][i]])
		desc.hydrophobic_ratio()
		hydrophobic_ratio_array.append(desc.descriptor[0][0])
	except:
		hydrophobic_ratio_array.append('')

database['hydrophobic_ratio'] = hydrophobic_ratio_array

print("Estimate hydrophobicity_profile_array")

#profile hydrophobicity
hydrophobicity_profile_array = []
for i in range(len(database)):
	try:
		desc = PeptideDescriptor([database['sequence'][i]], scalename='Eisenberg')
		desc.calculate_profile(prof_type='H')	
		hydrophobicity_profile_array.append(desc.descriptor[0][0])
	except:
		hydrophobicity_profile_array.append('')

database['hydrophobicity_profile'] = hydrophobicity_profile_array

print("Estimate hydrophobic_profile_array")
#profile hydrophobicity
hydrophobic_profile_array = []
for i in range(len(database)):
	try:
		desc = PeptideDescriptor([database['sequence'][i]], scalename='Eisenberg')
		desc.calculate_profile(prof_type='uH')	
		hydrophobic_profile_array.append(desc.descriptor[0][0])
	except:
		hydrophobic_profile_array.append('')

database['hydrophobic_profile'] = hydrophobic_profile_array

print("Export to csv")
database.to_csv(path_output+"4_add_features.csv", index=False)