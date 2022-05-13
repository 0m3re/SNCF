#!/usr/bin/python3
# convert hex to rgba between 0 and 1
from gi.repository import Gdk

def gdkrgba_to_hex(color):
    try :
        rgba_color = color.to_string()
        a,col1 = rgba_color.split('(')
        col1,col2,col3,col4 = col1.split(',')
        col4,b= col4.split(')')
        
        lst = [int(col1), int(col2), int(col3), int(float(col4)*255)]
        
        hex = '#%02x%02x%02x%02x' % (lst[0], lst[1], lst[2], lst[3])
    except :
        rgba_color = color.to_string()
        a,col1 = rgba_color.split('(')
        col1,col2,col3 = col1.split(',')
        col3,b= col3.split(')')
        
        lst = [int(col1), int(col2), int(col3)]
        
        hex = '#%02x%02x%02x' % (lst[0], lst[1], lst[2])
    
    return hex