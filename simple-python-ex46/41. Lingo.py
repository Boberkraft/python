from random import randint

words = 'quick lingo juice queue squid squad kicks juicy limbo jacks'.split()
word = words[randint(0, len(words))]

while 1:
    while 1:
        anwser = input(">>>")
        if len(anwser) == 5:
            break
    s = ''
    for index, letter in enumerate(anwser):
        if letter == word[index]:
            s += '[' + letter + ']'
        elif letter in word:
            s += '(' + letter + ')'
        else:
            s += letter
    print('Clue:', s)




