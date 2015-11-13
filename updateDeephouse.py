import os, re
import json
import pdb

def loadArrangement(arrPath):
    with open(arrPath, mode='r') as infile:
        arr = json.load(infile)
    return arr

for fname in os.listdir("."):
	if fname.endswith(".json"):
		arr = loadArrangement(fname)
		if 'path' in arr:
			del arr['path']
		for track in arr['tracks']:
			if 'role' in track and track['role'] == 'lead':
				for func in track['compositionFunctions']:
					if func['name'] == 'addJazzHarmonies':
						func['args'] = {
							"clip": "leadClip",
	                        "velocities": [
	                            8,
	                            38
	                        ],
	                        "pitchRange": [
	                            50,
	                            72
	                        ],
	                        "chordProgression": "chordProgression",
	                        "chordDurations": "CHORD_DURATIONS",
	                        "tonic": "tonic",
	                        "totalDur": "totalDur",
	                        "delayAmt": 0.01
	                    }
		with open(fname, 'w') as outfile:
			json.dump(arr, outfile, indent=4, sort_keys=True, separators=(',',':'))