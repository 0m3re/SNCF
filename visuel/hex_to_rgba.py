# convert hex to rgba between 0 and 1
def hex_to_rgba(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i+hlen//3], 16)/255 for i in range(0, hlen, hlen//3))