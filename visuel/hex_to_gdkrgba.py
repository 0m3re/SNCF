#!/usr/bin/python3
from gi.repository import Gdk

# convert hex to rgba between 0 and 1
def hex_to_gdkrgba(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    color_list = list(int(hex[i:i+hlen//3], 16)/255 for i in range(0, hlen, hlen//3))
    return Gdk.RGBA(*color_list)