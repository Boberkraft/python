# def rysuj(mapa):
#     for x in mapa:
#         for y in x:
#             print(y, end="")
#         print()
#
# rozmiar_mapy = 10
#
# mapa = [['-' for y in range(rozmiar_mapy)]for x in range(rozmiar_mapy)]
# rysuj(mapa)
# print(mapa)
import time

wonsz = 5
zwieksz = 1
while 1:
    print("|", end = '')
    for x in range(7):

        if x == wonsz:
            print('*', end = "")
        else:
            print(" ", end = "")
    wonsz += zwieksz
    if wonsz < 2 or wonsz > 5:
        if zwieksz == 1:
            zwieksz = -1
            wonsz -= 1
        else:
            zwieksz = 1
            wonsz += 1

    print('|')
    time.sleep(0.005)