import os, re
import json
import pdb

def loadArrangement(arrPath):
    with open(arrPath, mode='r') as infile:
        arr = json.load(infile)
    return arr

outJson = []
for fname in os.listdir("."):
	if fname.endswith(".json"):
		graphFiles = {}
		arr = loadArrangement(fname)
		for track in arr['tracks']:
			if 'role' in track:
				graphFiles[track['role']] = track['graphFiles']
		outName = fname.rstrip('.json').split('mutation')[-1]
		outJson.append(graphFiles)

with open("mutations.json", 'w') as outfile:
	json.dump(outJson, outfile, indent=4, sort_keys=True, separators=(',',':'))