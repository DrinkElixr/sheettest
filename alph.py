alp="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alpht=[]
for letter in alp:
    alpht.append(letter)
for letter in alp:
    for letter2 in alp:
        alpht.append(letter+letter2)
for letter1 in alp:
    for letter2 in alp:
        for letter3 in alp:
            alpht.append(letter1+letter2+letter3)

alph=alpht
def int_convert(v):
            if len(v)>0:
                v=int(v)
            else:
                v=0
            return v
def float_convert(v):
            if len(v)>0:
                try:
                    v=float(v)
                except:v=0.0
            else:
                v=0.0
            print(v)
            return v
def float_confirm(v):
    if type(v)==type(1.1):
        return v
    elif type(v)==type(1):
        return (float(v))
    else: float_convert(v)
def alph_finder(int):
    print(alph[int])
    return alph[int]

