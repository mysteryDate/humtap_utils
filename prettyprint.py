import json

def loadArrangement(arrPath):
    with open(arrPath, mode='r') as infile:
        arr = json.load(infile)
    return arr

arrPath = "deephouse_mutation03.json"
arr = loadArrangement(arrPath)

with open("pretty.json", 'w') as outfile:
	json.dump(arr, outfile, indent=4, sort_keys=True, separators=(',',':'))