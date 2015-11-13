import json, os, pdb

def loadArrangement(arrPath):
    with open(arrPath, mode='r') as infile:
        arr = json.load(infile)
    return arr

arrPath = "genreArrFilenameFeatures.json"
arr = loadArrangement(arrPath)

dh1 = arr['dance']['deephouse.json']
dh2 = arr['dance']['deephouse2.json']
dh3 = arr['dance']['deephouse3.json']

for fname in os.listdir("/Volumes/Hieronymus/Users/aaronk/Desktop/no duplicates.json/mutations/deephouse"):
	arr['dance'][fname] = dh1

for fname in os.listdir("/Volumes/Hieronymus/Users/aaronk/Desktop/no duplicates.json/mutations/deephouse2"):
	arr['dance'][fname] = dh2

for fname in os.listdir("/Volumes/Hieronymus/Users/aaronk/Desktop/no duplicates.json/mutations/deephouse3"):
	arr['dance'][fname] = dh3

with open("newFeatures.json", 'w') as outfile:
	json.dump(arr, outfile, indent=4, sort_keys=True, separators=(',',':'))