import os
import time


#Using external program caled jampal
#http://jampal.sourceforge.net/ptts.html
#and passing (piping) word to speech using shell command thats call ptts.vbs
def speak_ICAO(sentence, space_words, space_letter):
    d = {'a': 'alfa', 'b': 'bravo', 'c': 'charlie', 'd': 'delta', 'e': 'echo', 'f': 'foxtrot',
         'g': 'golf', 'h': 'hotel', 'i': 'india', 'j': 'juliett', 'k': 'kilo', 'l': 'lima',
         'm': 'mike', 'n': 'november', 'o': 'oscar', 'p': 'papa', 'q': 'quebec', 'r': 'romeo',
         's': 'sierra', 't': 'tango', 'u': 'uniform', 'v': 'victor', 'w': 'whiskey',
         'x': 'x-ray', 'y': 'yankee', 'z': 'zulu'}

    for word in sentence.split():
        for letter in word:
            os.system('echo ' + d[letter] + '|cscript "D:\programy\Jampal\ptts.vbs"')
            #you can use -r rate option for faster speech or slower -10 tp +10, default is 0

            time.sleep(space_letter)
        time.sleep(space_words)


speak_ICAO('moja mama i robi dobre jedzenie', 1, 0.2)

