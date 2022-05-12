#!/usr/bin/python3
from loadgui import problems
import matplotlib.pyplot as plt
import numpy as np

def pie_chart(directory, colors):
    h, i = problems(directory)
    fig = plt.figure()

    lst_data = []
    lst_value = []
    for j in range(len(h)):
        lst_data.append(h[j])
        lst_value.append(i[j])
    
    lst_value = np.array(lst_value)

    plt.pie(lst_value,colors=colors, autopct='%1.0f%%')

    fig.savefig(f'visuel/img/{directory}_pie_chart.png', transparent=True)
