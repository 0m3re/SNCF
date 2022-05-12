#!/usr/bin/python3
import json
import matplotlib.pyplot as plt
import numpy as np

def load(directory):
    with open(f'calculus/{directory}.txt') as json_file: # how to access the file 
        data = json.load(json_file)
        # get h and i from the data loop through the data
        lst_h = []
        lst_i = []
        for j in range(10):
            lst_h.append(data["disruptions_message"][f'data{j}'])
            lst_i.append(data["disruptions_message"][f'value{j}'] )


        return lst_h, lst_i

def pie_chart(directory, colors):
    h, i = load(directory)
    fig = plt.figure()

    lst_data = []
    lst_value = []
    for j in range(len(h)):
        lst_data.append(h[j])
        lst_value.append(i[j])
    
    lst_data = np.array(lst_data)
    lst_value = np.array(lst_value)

    plt.pie(lst_value,colors=colors, autopct='%1.0f%%')

    fig.savefig(f'visuel/img/{directory}_pie_chart.png', transparent=True)