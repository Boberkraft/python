from collections import defaultdict
import string

names = 'dog goldfish fucker hippotamus snake'.split()
def make_dic():
    dic = defaultdict(dict)
    for letter in [chr(x) for x in range(ord('a'), ord('z') + 1)]:
        dic[str(letter)] = {'start':0, 'end':0}
    for name in names:
        dic[name[0]]['start'] += 1
        dic[name[-1]]['end'] += 1
    return dic

def do_it(words, dic):
    last_letter = ''

    seq = []

    letter = ''
    for word2 in words:
        best = ['', 0]
        for rule, values in dic.items():
            if values['end'] == 0:
                values['end'] = 0.1
            if values['start']/values['end'] > best[1]:
                for word in words:
                    if word.endswith(rule):
                        if letter == '' or word.startswith(letter):
                            best = [rule, values['start'] / values['end']]

        for word in words:
            if word.endswith(best[0]):
                if letter == '':
                    seq.append(word)
                    letter = word[-1]
                    words.remove(word)

                else:
                    if word.startswith(letter):
                        seq.append(word)
                        letter = word[-1]
                        words.remove(word)

                break
    print('next', letter)
    return seq

def show(test):
    for y,i in test.items():
        print(y,i)

x = make_dic()
show(x)
print('wyszlo:',do_it(names, x))
print('powinno', )
