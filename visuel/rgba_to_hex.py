# convert rgba to hex
def rgba_to_hex(rgba):
    hex = '#%02x%02x%02x%02x' % (rgba[0], rgba[1], rgba[2], rgba[3])
    return hex