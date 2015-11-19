# Run from utils directory
import json, pdb
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import pdb

PATH_TO_DATA = ["data/electro_output.txt", "data/rock_output.txt", "data/hiphop_output.txt"]
sum_arrangements = False

def avg(li):
    return sum(li) / float(len(li))

def loadData(path):
    data = []
    for p in path:
        with open(p, "r") as infile:
            data = data + json.load(infile)

    return data

def splitDataByArrangement(rawData):
    # Returns a dictionary of arrays:
    # data = {arr1: [render1, render2...], arr2: [render1, render2...], ...}

    data = {}
    for project in rawData:
        # Create entry if it does not exist
        if project['arr'] not in data:
            data[project['arr']] = []
        dataToAdd = {
            'totalTime': float(project['totalTime']),
            'loopLength': float(project['loopLength']),
            'vsts': float(project['vsts']),
            'hum': project['hum'],
            'genre': project['genre'],
            'times': {
                'init': float(project['Benchmarks']['Breakdown']['Initialization']),
                'audio': float(project['Benchmarks']['Breakdown']['Audio Processing']),
                'other': float(project['Benchmarks']['Total processing time in s']) 
                    - float(project['Benchmarks']['Breakdown']['Initialization']) 
                    - float(project['Benchmarks']['Breakdown']['Audio Processing'])
            }
        }
    data[project['arr']].append(dataToAdd)

    return data

def averageArrangmentData(data):
    # data = {arr1: [render1, render2...], arr2: [render1, render2...], ...}
    # Adds together parameters of each rendering
    # return avgData = {arr1: {'totalTime': 8, 'vsts': 20 ...}, arr2: {'totalTime':20, 'vsts': 15 ...}, ...}

    avgData = {}
    for arr in data:
        avgData[arr] = { 'genre': data[arr][0]['genre'] }
        avgData[arr]['totalTime']       = avg( [d['totalTime'] for d in data[arr]] )
        avgData[arr]['loopLength']      = avg( [d['loopLength'] for d in data[arr]] )
        avgData[arr]['vsts']            = avg( [d['vsts'] for d in data[arr]] )
        avgData[arr]['times']           = {
                'init' : avg( d['init'] for d in data[arr]['times']),
                'audio' : avg( d['audio'] for d in data[arr]['times']),
                'other' : avg( d['other'] for d in data[arr]['times'])
        }
    return avgData

def main():
    rawData = loadData(PATH_TO_DATA)

    rawData = splitDataByArrangement(rawData)
    avgData = averageArrangmentData(rawData)

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