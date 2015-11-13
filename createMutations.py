import json
import pdb
import itertools

leads = [
	"trance_lead1.graph",
	"trance_lead2.graph",
	"trance_lead3.graph",
	"trance_lead4.graph"
]

basses = [
	"trance_bass1.graph",
	"trance_bass2.graph",
	"trance_bass3.graph",
	"trance_bass4.graph"
]

chords = [
	"trance_stab1.graph",
	"trance_stab2.graph",
	"trance_stab3.graph",
	"trance_stab4.graph"
]

possibilities = list(itertools.product(*[leads, basses, chords]))

mutationFile = []

for insts in possibilities:
	arr = {}
	arr['lead'] = [insts[0]]
	arr['bass'] = [insts[1]]
	arr['chords'] = [insts[2]]
	mutationFile.append(arr)

with open("trance_mutations.json", 'w') as outfile:
	json.dump(mutationFile, outfile, indent=4, sort_keys=True, separators=(',',':'))


