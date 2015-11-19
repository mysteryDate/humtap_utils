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

    data = {}
    for project in rawData:
        if project['arr'] not in data:
            # data[project['arr']] = []
            data[project['arr']] = {
                'totalTime': project['totalTime'],
                'loopLength': project['loopLength'],
                'vsts': project['vsts'],
                'genre': project['genre'],
                'init_time': project['Benchmarks']['Breakdown']['Initialization'],
                'audio_time': project['Benchmarks']['Breakdown']['Audio Processing'],
                # 'hum': project['hum']
                'numRenders': 1
            }
        else:
            data[project['arr']]['totalTime'] += project['totalTime']
            data[project['arr']]['loopLength'] += project['loopLength']
            data[project['arr']]['vsts'] += project['vsts']
            data[project['arr']]['init_time'] += project['Benchmarks']['Breakdown']['Initialization']
            data[project['arr']]['audio_time'] += project['Benchmarks']['Breakdown']['Audio Processing']
            data[project['arr']]['numRenders'] += 1
        # dataToAdd = {
        #     'totalTime': datum['totalTime'],
        #     'loopLength': datum['loopLength'],
        #     'vsts': datum['vsts'],
        #     'hum': datum['hum']
        # }
        # data[datum['arr']].append(dataToAdd)

    graphData = []
    for arr in data:
        trace = go.Scatter(
            x = [d['vsts'] for d in data[arr]],
            y = [d['totalTime'] for d in data[arr]],
            mode = 'markers',
            name = arr,
            # text = ["Hum:\t"+d['hum']+"<br>Length:\t"+str(round(float(d['loopLength'])/44100,2))+"s" for d in data[arr]]
        )
        graphData.append(trace)
    # genres = ['electro','rock','hiphop']
    # for genre in genres:
    #     trace = go.Scatter(
    #         x = [float(d['vsts'])/d['numRenders'] for d in data.values() if d['genre'] == genre],
    #         y = [d['totalTime']/d['numRenders'] for d in data.values() if d['genre'] == genre],
    #         mode = 'markers',
    #         name = genre,
    #         text = [d for d in data if data[d]['genre'] == genre]
    #     )
    #     graphData.append(trace)

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

    # py.sign_in("MysteryDate", "a6fd7sm5jr")

    # fig = go.Figure(data=graphData, layout=layout)
    # plot_url = py.plot(fig, filename="Render times by vsts for all arrangements by genre (averaged)")

main()