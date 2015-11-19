# Run from utils directory
import json, pdb
import plotly.plotly as py
import plotly.graph_objs as go
# import numpy as np
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
            'init_time': float(project['Benchmarks']['Breakdown']['Initialization']),
            'audio_time': float(project['Benchmarks']['Breakdown']['Audio Processing']),
            'other_time': float(project['Benchmarks']['Total processing time in s']) 
                    - float(project['Benchmarks']['Breakdown']['Initialization']) 
                    - float(project['Benchmarks']['Breakdown']['Audio Processing']),
            'non_time' :  float(project['totalTime']) - float(project['Benchmarks']['Total processing time in s'])
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
        avgData[arr]['init_time']       = avg( [d['init_time'] for d in data[arr]])
        avgData[arr]['audio_time']      = avg( [d['audio_time'] for d in data[arr]])
        avgData[arr]['other_time']      = avg( [d['other_time'] for d in data[arr]])
        avgData[arr]['non_time']        = avg( [d['non_time'] for d in data[arr]])
    return avgData

def createTracesForRaw(data, xvariable, yvariable):
    graphData = []
    for arr in data:
        trace = go.Scatter(
            x = [d[xvariable] for d in data[arr]],
            y = [d[yvariable] for d in data[arr]],
            mode = 'markers',
            name = arr,
            text = [
                "Hum:\t"+d['hum']
                +"<br>Length:\t"+str(round(float(d['loopLength'])/44100,2))
                +"<br>Render time:\t"+str(d['totalTime']) 
                +"s<br>Num VSTs:\t"+str(d['vsts'])
                    for d in data[arr]]
        )
        graphData.append(trace)
    return graphData

def createTraceForAvg(data, xvariable, yvariable, byGenre=False, name=None):
    if not byGenre:
        trace = go.Scatter(
            x = [d[xvariable] for d in data.values()],
            y = [d[yvariable] for d in data.values()],
            mode = 'markers',
            name = name,
            text  = [
                "Arrangement:\t"+ n
                +"<br>AVG Length:\t"+str(round(d['loopLength']/44100,2))
                +"<br>AVG Render time:\t"+str(round(d['totalTime'],2)) 
                +"s<br>AVG Num VSTs:\t"+str(d['vsts']) for (n,d) in zip(data,data.values())]
        )
        return [trace]

    genres = ['electro','rock','hiphop']
    graphData = []
    for genre in genres:
        trace = go.Scatter(
            x = [d[xvariable] for d in data.values() if d['genre'] == genre],
            y = [d[yvariable] for d in data.values() if d['genre'] == genre],
            mode = 'markers',
            name = genre,
            text = [d for d in data if data[d]['genre'] == genre]
        )
        graphData.append(trace)
    return graphData

def main():
    rawData = loadData(PATH_TO_DATA)

    rawData = splitDataByArrangement(rawData)
    avgData = averageArrangmentData(rawData)

    # graphData = createTracesForRaw(rawData, 'loopLength','audio_time')
    graphData = createTraceForAvg(avgData, 'audio_time', 'totalTime', name="audio")
    graphData += createTraceForAvg(avgData, 'init_time', 'totalTime', name="init")
    graphData += createTraceForAvg(avgData, 'other_time', 'totalTime', name="other")
    graphData += createTraceForAvg(avgData, 'non_time', 'totalTime', name="non")

    layout = go.Layout(
        title='Total Rendering Time vs Audio/Initialization Time',
        hovermode='closest',
        xaxis=dict(
            title='Time Spent on Stage (s)'
        ),
        yaxis=dict(
            title='Total Rendering Time (s)'
        ),
    )

    py.sign_in("MysteryDate", "a6fd7sm5jr")

    fig = go.Figure(data=graphData, layout=layout)
    plot_url = py.plot(fig, filename="Sources of Rendering Time")

main()