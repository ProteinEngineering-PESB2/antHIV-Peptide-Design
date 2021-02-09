import pandas as pd
import sys
import os
from Bio import pairwise2
from Bio.pairwise2 import format_alignment

print("Read doc csv")
dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

sequences_matrix = [sequence for sequence in dataset['sequence']]

sequence_full = "AVGIGALFLGFLGAAGSTMGAASMTLTVQARQLLSGIVQQQNNLLRAIEAQQHLLQLTVWGIKQLQARILAVERYLKDQQLLGIWGCSGKLICTTAVPWNASWSNKSLEQIWNHTTWMEWDREINNYTSLIHSLIEESQNQQEKNEQELLELDKWASLWNWFNITNWLWYIKLFIMIVGGLVGLRIVFAVLSIVNRVRQGYSPLSFQTHLPTPRGPDRPEGIEEEGGERDRDRSIRLVNGSLALIWDDLRSLCLFSYHRLRDLLLIVTRIVELLGRRGWEALKYWWNLLQYWSQELKNSAVSLLNATAIAVAEGTDRVIEVVQGACRAIRHIPRRIRQGLERILL"

#define domains
domains = {'fp_domain': sequence_full[0:16], 'nhr_domain': sequence_full[16:70], 'tm_domain' : sequence_full[172:193], "cp_domain": sequence_full[194:-1], "loop1_PBD_CHR" : sequence_full[70:155], "CHR_LPB_loop2": sequence_full[124:172]}

keys_domain = [domain for domain in domains]

matrix_response = []

print("Make alignments")
for sequence in sequences_matrix:	
	print(sequence, "sequence to process")
	print("Process sequence: ", sequence)

	row_alignment = []
	for domain in keys_domain:
		print("Aling with domain: ", domain)		
		alignments = pairwise2.align.globalms(domains[domain], sequence, 2, -1, -.5, -.1, score_only=True)		
		row_alignment.append(alignments)

	matrix_response.append(row_alignment)

print("Export results")
summary_alignment = pd.DataFrame(matrix_response, columns=keys_domain)
summary_alignment['sequence'] = sequences_matrix

summary_alignment.to_csv(path_output+"1_summary_alignment_with_pairwise2.csv", index=False)