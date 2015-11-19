# Run from utils directory
import json, pdb
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import pdb

PATH_TO_DATA = ["data/electro_output.txt", "data/rock_output.txt", "data/hiphop_output.txt"]

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
            data[project['arr']] = []
        #     data[project['arr']] = {
        #         'totalTime': float(project['totalTime']),
        #         'loopLength': float(project['loopLength']),
        #         'vsts': float(project['vsts']),
        #         'genre': project['genre'],
        #         'init_time': float(project['Benchmarks']['Breakdown']['Initialization']),
        #         'audio_time': float(project['Benchmarks']['Breakdown']['Audio Processing']),
        #         'hum': project['hum']
        #         'numRenders': 1
        #     }
        # else:
        #     data[project['arr']]['totalTime'] += float(project['totalTime'])
        #     data[project['arr']]['loopLength'] += float(project['loopLength'])
        #     data[project['arr']]['vsts'] += float(project['vsts'])
        #     data[project['arr']]['init_time'] += float(project['Benchmarks']['Breakdown']['Initialization'])
        #     data[project['arr']]['audio_time'] += float(project['Benchmarks']['Breakdown']['Audio Processing'])
        #     data[project['arr']]['numRenders'] += 1
        dataToAdd = {
            'totalTime': float(project['totalTime']),
            'loopLength': float(project['loopLength']),
            'vsts': float(project['vsts']),
            'hum': project['hum'],
            'genre': project['genre'],
            'init_time': float(project['Benchmarks']['Breakdown']['Initialization']),
            'audio_time': float(project['Benchmarks']['Breakdown']['Audio Processing'])
        }
        data[project['arr']].append(dataToAdd)

    graphData = []
    for arr in data:
        trace = go.Scatter(
            x = [d['init_time'] for d in data[arr]],
            y = [d['audio_time'] for d in data[arr]],
            mode = 'markers',
            name = arr,
            text = [
                "Hum:\t"+d['hum']
                +"<br>Length:\t"+str(round(float(d['loopLength'])/44100,2))+"s<br>"
                +"Num VSTs:\t"+str(d['vsts'])
                +"<br>Render time:\t"+str(d['totalTime']) for d in data[arr]]
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
        title='Audio Processing Time vs Initialization Time',
        hovermode='closest',
        xaxis=dict(
            title='Time Spent Initializing (nearest whole second)'
        ),
        yaxis=dict(
            title='Time Spent Audio Processing (nearest whole second)'
        ),
    )

    py.sign_in("MysteryDate", "a6fd7sm5jr")

    fig = go.Figure(data=graphData, layout=layout)
    plot_url = py.plot(fig, filename="Audio Processing Time vs Initialization Time")

main()