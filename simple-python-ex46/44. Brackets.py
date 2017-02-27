from random import randint

def generate(N):
    seq = ''
    for x in range(N * 2):
        if randint(0,1):
            seq += '['
        else:
            seq += ']'
    return seq

def analise(sequence):
    #if one bracket is missleading it interupts whole procces and return not ok
    num = 0
    for bracket in sequence:
        if bracket == '[':
            num += 1
        else:
            num -= 1
        if num < 0:
            return "NOT OK"
    return 'OK'
brac = generate(10)
print(analise('[[][]]'))
