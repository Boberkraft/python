import sys

low, high = map(int, input().split())

while True:
    avg = (high+low)//2
    print(avg)
    res = int(input())
    if res == 1:
        low = avg
    if res == -1:
        high = avg
    if res == 0:
        quit()

