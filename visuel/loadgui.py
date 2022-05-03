#! /usr/bin/python3

import json

def load(directory):
    with open(f'calculus/{directory}.txt') as json_file: # how to access the file 
        data = json.load(json_file)
        a = data["vehicle"]
        b = data["stop_times"]
        c = data["disruptions"]
        d = data["%_vehicle"]
        e = data["impacted_stop"]
        f = data["%_stop_times"]
        g = data["routes"]
        # h = data["disruptions_message"]['data0']        # loop through the data
        # i = data["disruptions_message"]['value0']       # loop through the data
        # j = data["citi_impacted"]['data0']              # loop through the data 
        # k = data["citi_impacted"]['value0']             # loop through the data
        # jj = data["citi_impacted"]['lat0']              # loop through the data 
        # kk = data["citi_impacted"]['lon0']              # loop through the data
        # l = data["citi_time_impacted"]['data0']         # loop through the data
        # m = data["citi_time_impacted"]['value0']        # loop through the data 
        # ll = data["citi_time_impacted"]['lat0']         # loop through the data 
        # mm = data["citi_time_impacted"]['lon0']         # loop through the data
        n = data["citi_time_impacted_tot"]
        # o = data["disruptions_severity_name"]['data0']  # loop through the data
        # p = data["disruptions_severity_name"]['value0'] # loop through the data
        # q = data["routes_max_retard"]['data0']          # loop through the data
        # r = data["routes_max_retard"]['value0']         # loop through the data
        # qq = data["routes_max_retard"]['lat0']          # loop through the data
        # rr = data["routes_max_retard"]['lon0']          # loop through the data
        # s = data["routes_min_retard"]['data0']          # loop through the data ?
        # t = data["routes_min_retard"]['value0']         # loop through the data
        # ss = data["routes_min_retard"]['lat0']          # loop through the data ?
        # tt = data["routes_min_retard"]['lon0']          # loop through the data
        u = data["%_routes"]
    
    return a, b, c, d, e, f, g, n, u

def city_time(directory):
    with open(f'calculus/{directory}.txt') as json_file: # how to access the file 
        data = json.load(json_file)
        lst_data = []
        lst_value = []
        lst_lat = []
        lst_lon = []
        for i in range(10):
            lst_data.append(data["citi_time_impacted"][f"data{i}"])
            lst_value.append(data["citi_time_impacted"][f"value{i}"])
            lst_lat.append(data["citi_time_impacted"][f"lat{i}"])
            lst_lon.append(data["citi_time_impacted"][f"lon{i}"])
            
        return lst_data, lst_value, lst_lat, lst_lon
        

# print('a',a)
# print('b',b)
# print('c',c)
# print('d',d)
# print('e',e)
# print('f',f)
# print('g',g)
# print('h',h)
# print('i',i)
# print('j',j)
# print('k',k)
# print('jj',jj)
# print('kk',kk)
# print('l',l)
# print('m',m)
# print('ll',ll)
# print('mm',mm)
# print('n',n)
# print('o',o)
# print('p',p)
# print('q',q)
# print('r',r)
# print('qq',qq)
# print('rr',rr)
# print('s',s)
# print('t',t)
# print('ss',ss)
# print('tt',tt)
# print('u',u)
