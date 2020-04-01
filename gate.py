#AND gate
def GAND(a, b):
    if a == '1':
        if b == '1':
            out = '1'
        elif (b == 'D'):
            out = 'D'
        elif (b == 'D_bar'):
            out = 'D_bar'
        elif (b == 'X'):
            out = 'X'
        elif (b == '0'):
            out = '0'
    elif a == '0':
        out = '0'
    elif a == 'X':
        if b == '0':
            out = '0'
        else:
            out = 'X'
    elif a == 'D':
        if b == '1':
            out = 'D'
        elif (b == 'D'):
            out = 'D'
        elif (b == 'D_bar'):
            out = '0'
        elif (b == 'X'):
            out = 'X'
        elif (b == '0'):
            out = '0'
    elif a == 'D_bar':
        if b == '1':
            out = 'D_bar'
        elif (b == 'D'):
            out = '0'
        elif (b == 'D_bar'):
            out = '0'
        elif (b == 'X'):
            out = 'X'
        elif (b == '0'):
            out = '0'
    return out

#OR gate
def GOR(a, b):
    if a == '1':
        out = '1'
    elif a == '0':
        if b == '1':
            out = '1'
        elif (b == 'D'):
            out = 'D'
        elif (b == 'D_bar'):
            out = 'D_bar'
        elif (b == 'X'):
            out = 'X'
        elif (b == '0'):
            out = '0'
    elif a == 'X':
        if b == '1':
            out = '1'
        else:
            out = 'X'
    elif a == 'D':
        if b == '1':
            out = '1'
        elif (b == 'D'):
            out = 'D'
        elif (b == 'D_bar'):
            out = '1'
        elif (b == 'X'):
            out = 'X'
        elif (b == '0'):
            out = 'D'
    elif a == 'D_bar':
        if b == '1':
            out = '1'
        elif (b == 'D'):
            out = '1'
        elif (b == 'D_bar'):
            out = 'D_bar'
        elif (b == 'X'):
            out = 'X'
        elif (b == '0'):
            out = 'D_bar'
    return out

#XOR gate
def GXOR(a, b):
    if a == '1':
        if b == '1':
            out = '0'
        elif (b == 'D'):
            out = 'D_bar'
        elif (b == 'D_bar'):
            out = 'D'
        elif (b == 'X'):
            out = 'X'
        elif (b == '0'):
            out = '1'
    elif a == '0':
        if b == '1':
            out = '1'
        elif (b == 'D'):
            out = 'D'
        elif (b == 'D_bar'):
            out = 'D_bar'
        elif (b == 'X'):
            out = 'X'
        elif (b == '0'):
            out = '0'
    elif a == 'X':
        out = 'X'
    elif a == 'D':
        if b == '1':
            out = 'D_bar'
        elif (b == 'D'):
            out = '0'
        elif (b == 'D_bar'):
            out = '1'
        elif (b == 'X'):
            out = 'X'
        elif (b == '0'):
            out = 'D'
    elif a == 'D_bar':
        if b == '1':
            out = 'D'
        elif (b == 'D'):
            out = '1'
        elif (b == 'D_bar'):
            out = '0'
        elif (b == 'X'):
            out = 'X'
        elif (b == '0'):
            out = 'D'
    return out

#NOT gate
def GNOT(a):
    if a == '1':
        out = '0'
    elif a == '0':
        out = '1'
    elif a == 'X':
        out = 'X'
    elif a == 'D':
        out = 'D_bar'
    elif a == 'D_bar':
        out = 'D'
    return out