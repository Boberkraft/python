import os
import random
import sys
import threading

def eprint(*args):
    '''Funkcja pozwalająca podglądaj wyjście w konsoli'''
    print(*args, file=sys.stderr)


def deviser(max, r, w):
    sys.stdin = r
    sys.stdout = w
    # with that i can just use print() and input()
    eprint('deviser',r, w)

    with open('deviser.txt', 'w') as f:
        to_be_guessed = int(max * random.random() + 1)
        eprint('BOT1: my hidden number is', to_be_guessed)
        f.write('My hidden number is ' + str(to_be_guessed) + '\n')
        guess = 0
        while guess != to_be_guessed:
            eprint('BOT1: waiting for guess', guess)

            guess = r.readline()[:-1]

            eprint('BOT1: he guessed', guess)
            guess = int(guess)

            f.write('He tried to guess ' + str(guess) + "\n")
            eprint('BOT1: replying')
            w.flush()
            if guess > 0:
                if guess > to_be_guessed:
                    w.write('1\n')
                elif guess < to_be_guessed:
                    w.write('-1\n')
                else:
                    w.write('0\n')

                w.flush()
            else:
                w.write('99\n')
                break


def guesser(max, r, w):

    eprint('guesser',r, w)
    sys.stdin = r
    sys.stdout = w
    # with that i can just use print() and input()
    with open('guesser.txt', 'w') as f:
        bottom, top = 0, max
        fuzzy = 10
        res = 1
        while res != 0:
            guess = (bottom + top) // 2
            eprint('BOT2: i guessed', guess)
            w.write(str(guess) + '\n')
            f.write('Guessing ' + str(guess) + '\n')
            w.flush()
            eprint('BOT2: is ma answer good?')
            res = int(r.readline()[:-1])
            eprint('BOT2: Now i know if my answer is good', res)
            if res == -1:
                bottom = guess
            elif res == 1:
                top = guess
            elif res == 0:
                f.write('Wanted number is %d' % guess)
            else:
                eprint('Input not correct')
                f.write("Something's wrong")


n = 100

r, w = os.pipe()
r1, w1 = os.pipe()

r, w = os.fdopen(r, 'r'), os.fdopen(w, 'w')
r1, w1 = os.fdopen(r1, 'r'), os.fdopen(w1, 'w')

thread_parent = threading.Thread(target=deviser, args=(n, r, w1))
thread_child = threading.Thread(target=guesser, args=(n, r1, w))

thread_parent.start()
thread_child.start()

