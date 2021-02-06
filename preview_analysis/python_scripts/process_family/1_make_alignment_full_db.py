import pandas as pd
import sys
from Bio import pairwise2
from Bio.pairwise2 import format_alignment

sequence_full = "AVGIGALFLGFLGAAGSTMGAASMTLTVQARQLLSGIVQQQNNLLRAIEAQQHLLQLTVWGIKQLQARILAVERYLKDQQLLGIWGCSGKLICTTAVPWNASWSNKSLEQIWNHTTWMEWDREINNYTSLIHSLIEESQNQQEKNEQELLELDKWASLWNWFNITNWLWYIKLFIMIVGGLVGLRIVFAVLSIVNRVRQGYSPLSFQTHLPTPRGPDRPEGIEEEGGERDRDRSIRLVNGSLALIWDDLRSLCLFSYHRLRDLLLIVTRIVELLGRRGWEALKYWWNLLQYWSQELKNSAVSLLNATAIAVAEGTDRVIEVVQGACRAIRHIPRRIRQGLERILL"

dataset = pd.read_csv(sys.argv[1])
name_output = sys.argv[2]

#define domains
domains = {'fp_domain': sequence_full[0:16], 'nhr_domain': sequence_full[16:70], 'chr_domain' : sequence_full[116:162], 'tm_domain' : sequence_full[172:193], 'loop2' : sequence_full[162:172],'loop1' :sequence_full[70:116]}

keys_domain = [domain for domain in domains]

matrix_response = []

sequence_data = []

for i in range(len(dataset)):

	sequence = dataset['sequence'][i]	

	sequence_data.append(sequence)
	print("Process sequence: ", sequence)

	row_alignment = []
	for domain in keys_domain:
		print("Aling with domain: ", domain)		
		alignments = pairwise2.align.globalms(domains[domain], sequence, 2, -1, -.5, -.1, score_only=True)		
		row_alignment.append(alignments)

	matrix_response.append(row_alignment)

summary_alignment = pd.DataFrame(matrix_response, columns=keys_domain)
summary_alignment['sequence'] = sequence_data

summary_alignment.to_csv(name_output, index=False)