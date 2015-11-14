import json, pdb
import plotly.plotly as plotly
import plotly.graph_objs as go
import numpy as np
import math

MIN_TEMPO = 60
MAX_TEMPO = 220
def main():

	with open("genreArrFilenameFeatures.json", 'r') as infile:
		data = json.load(infile)

	with open("tempi_dist.txt", "r") as infile:
		userTempos = infile.readlines()

	nearest5s = [5 * int(math.floor(float(x)/5)) for x in userTempos]
	tempoDistribution = {}
	for tempo in nearest5s:
		if tempo not in tempoDistribution:
			tempoDistribution[tempo] = 0
		tempoDistribution[tempo] += 1
	# pdb.set_trace()

	genre = "dance"
	bpms = []
	for arr in data[genre]:
		entry = (arr, 
			(data[genre][arr]['bpmRange']['min'], data[genre][arr]['bpmRange']['max']),
			data[genre][arr]["customProbability"]
		)
		bpms.append(entry)

	plotData = []
	lineData = []
	allx = [_ for _ in range(MIN_TEMPO, MAX_TEMPO + 1)]
	ytotal = [0 for x in allx]
	sortedBpms = sorted(bpms, key=lambda arr: arr[1][0])
	for arr in sortedBpms:
		ytotal = [arr[2] + y if x > arr[1][0] and x < arr[1][1] else y for (x,y) in zip(allx, ytotal)]
		xvalues = [x for x in range(arr[1][0], arr[1][1] + 1)]
		yvalues = [ytotal[x - MIN_TEMPO] for x in xvalues]
		lineTrace = go.Scatter(
			x = xvalues,
			y = yvalues,
			mode = 'lines',
			line = dict(width=1),
			hoverinfo = 'name',
			showlegend = False,
			# fill = 'tonexty',
			name = arr[0].split('.json')[0]
		)
		fill = go.Scatter(
			x = allx,
			y = ytotal,
			mode = 'lines',
			line = dict(width=0),
			hoverinfo = 'none',
			fill = 'tonexty',
			name = arr[0].split('.json')[0]
		)
		plotData.append(fill)
		plotData.append(lineTrace)

	layout = go.Layout(
		showlegend=True,
		xaxis=dict(type='linear', range=[MIN_TEMPO,160], dtick=5),
		yaxis=dict(type='linear', range=[0, 8], dtick=1),
	)

	plotly.sign_in("MysteryDate", "a6fd7sm5jr")

	fig = go.Figure(data=plotData, layout=layout)
	plot_url = plotly.plot(fig, filename="{gen} bpms".format(gen=genre))

main()	
# pdb.set_trace()