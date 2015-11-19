# Run from utils directory
import json, pdb
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import pdb

PATH_TO_DATA = ["../data/electro_output.txt", "../data/rock_output.txt", "../data/hiphop_output.txt"]

def loadData(path):
    data = []
    for p in path:
        with open(p, "r") as infile:
            data = data + json.load(infile)

    return data

def main():
    rawData = loadData(PATH_TO_DATA)

    arrangementData = {}
    for datum in rawData:
        if datum['arr'] not in arrangementData:
            # arrangementData[datum['arr']] = []
            arrangementData[datum['arr']] = {
                'totalTime': datum['totalTime'],
                'loopLength': datum['loopLength'],
                'vsts': datum['vsts'],
                'genre': datum['genre'],
                # 'hum': datum['hum']
                'numRenders': 1
            }
        else:
            arrangementData[datum['arr']]['totalTime'] += datum['totalTime']
            arrangementData[datum['arr']]['loopLength'] += datum['loopLength']
            arrangementData[datum['arr']]['vsts'] += datum['vsts']
            arrangementData[datum['arr']]['numRenders'] += 1
        # dataToAdd = {
        #     'totalTime': datum['totalTime'],
        #     'loopLength': datum['loopLength'],
        #     'vsts': datum['vsts'],
        #     'hum': datum['hum']
        # }
        # arrangementData[datum['arr']].append(dataToAdd)

    graphData = []
    # for arr in arrangementData:
    #     trace = go.Scatter(
    #         x = [d['vsts'] for d in arrangementData[arr]],
    #         y = [d['totalTime'] for d in arrangementData[arr]],
    #         mode = 'markers',
    #         name = arr,
    #         # text = ["Hum:\t"+d['hum']+"<br>Length:\t"+str(round(float(d['loopLength'])/44100,2))+"s" for d in arrangementData[arr]]
    #     )
    #     graphData.append(trace)
    genres = ['electro','rock','hiphop']
    for genre in genres:
        trace = go.Scatter(
            x = [float(d['vsts'])/d['numRenders'] for d in arrangementData.values() if d['genre'] == genre],
            y = [d['totalTime']/d['numRenders'] for d in arrangementData.values() if d['genre'] == genre],
            mode = 'markers',
            name = genre,
            text = [d for d in arrangementData if arrangementData[d]['genre'] == genre]
        )
        graphData.append(trace)

    layout = go.Layout(
        title='Render times by number of VSTs by arrangement',
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
    plot_url = py.plot(fig, filename="Render times by vsts for all arrangements by genre (averaged)")

main()