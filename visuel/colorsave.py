#!/usr/bin/python3

import json

def colorsave(jour, color_map1, color_map2, color_pie):
    a = [color_map1, color_map2, color_pie]
    b = ['map1', 'map2', 'pie']
    data_dict = {}
    for i in range(3):
        for j in range(len(a[i])):
            data_dict.update({f'{b[i]}_{j}': a[i][j]})
   
        with open(f'visuel/colors/colors_{jour}.json', 'w') as f:
            json.dump(data_dict, f)