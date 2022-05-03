#!/usr/bin/python3

from html2image import Html2Image
import folium
from PIL import Image
import os

hti = Html2Image()
carte= folium.Map(location=[46.6423, 2.2549],zoom_start=6)

def photo(file_name, lst_lat, lst_lon):
    for i in range(len(lst_lat)):
        folium.Marker([lst_lat[i], lst_lon[i]],icon=folium.Icon(color='green')).add_to(carte)


    carte.save(f'{file_name}.html')
    hti.screenshot(url=f'{file_name}.html', save_as=f'{file_name}.png')

    im = Image.open(rf"{file_name}.png")
    left = 597
    top = 199
    right = 1348
    bottom = 916

    im1 = im.crop((left, top, right, bottom))

    image_size = im1.resize((500, 475))
    image_size.save(f'{file_name}.png')

    os.rename(f'{file_name}.png', f'visuel/img/{file_name}.png')
    os.remove(f'{file_name}.html')
