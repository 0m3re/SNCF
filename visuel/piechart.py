#!/usr/bin/python3
from loadgui import problems
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os

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

    fig.savefig(f'pie_chart.png', transparent=True)

    im = Image.open(r"pie_chart.png")
    left = 165
    top = 80
    right = 490
    bottom = 405

    im1 = im.crop((left, top, right, bottom))

    image_size = im1.resize((500, 500))
    image_size.save('pie_chart.png')

    os.rename('pie_chart.png', f'visuel/img/{directory}_pie_chart.png')
