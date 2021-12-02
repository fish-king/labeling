def RGB_to_Hex(rgb):
    color = '#'
    for i in rgb:
        color += str(hex(i))[-2:].replace('x', '0').upper()
    return color

def clip(x, min, max):
    if x < min:
        x = min
    if x > max:
        x = max
    return x