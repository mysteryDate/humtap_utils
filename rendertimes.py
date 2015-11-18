# Run from utils directory
import json, pdb
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import pdb

PATH_TO_DATA = "../data/electro_output.txt"

def loadData(path):
    with open(path, "r") as infile:
        data = json.load(infile)

    return data

def main():
    rawData = loadData(PATH_TO_DATA)

    arrangementData = {}
    for datum in rawData:
        if datum['arr'] not in arrangementData:
            arrangementData[datum['arr']] = []
        dataToAdd = {
            'totalTime': datum['totalTime'],
            'loopLength': datum['loopLength'],
            'vsts': datum['vsts'],
            'hum': datum['hum']
        }
        arrangementData[datum['arr']].append(dataToAdd)

    graphData = []
    for arr in arrangementData:
        trace = go.Scatter(
            x = [d['vsts'] for d in arrangementData[arr]],
            y = [d['totalTime'] for d in arrangementData[arr]],
            mode = 'markers',
            name = arr,
            text = ["Hum:\t"+d['hum']+"<br>Length:\t"+str(round(float(d['loopLength'])/44100,2))+"s" for d in arrangementData[arr]]
        )
        graphData.append(trace)

    layout = go.Layout(
        title='Render times by number of VSTs for electro',
        hovermode='closest',
        xaxis=dict(
            title='Number of VSTs'
        ),
        yaxis=dict(
            title='Render time (s)'
        ),
    )

    py.sign_in("MysteryDate", "a6fd7sm5jr")

    fig = go.Figure(data=graphData, layout=layout)
    plot_url = py.plot(fig, filename="Render times by vsts for electro (improved)")

main()