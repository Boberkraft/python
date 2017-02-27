import string

def max(a,b):
    if a > b: return a
    else: return b

def max_of_three(a,b,c):
    x = b
    if a > b: x = a
    if c > x: x = c
    return x

def len(x):
    i = 0
    for a in x:
        i += 1
    return i

def sum(numbers):
    x = 0
    for num in numbers:
        x += num
    return x

def multiply(numbers):
    x = 1
    for num in numbers:
        x *= num
    return x

def isVovel(letter):
    vovels = 'aeyiou'
    if letter in vovels: return True
    else: return False

def translate(word):
    word = word.lower()
    consonats = 'BCDFGHJKLMNPQRSTVWXYZ'.lower()
    remixed = ""
    for letter in word:
        if letter in consonats:
            remixed += letter + 'o' + letter
        else:
            remixed += letter
    return remixed

def reverse(toReverse):
    x = ''
    for letter in toReverse:
        x = letter + x
    return x

def reverse1(toReverse):
    x = ''
    for num in range(0,len(toReverse)):
        x += toReverse[-(num + 1)]
    return x

def reverse2(toReverse):
    return toReverse[::-1]

def is_palindrome(word):
    x = True if reverse1(word) == word else False
    return x

def is_member(value, list):
    for x in list:
        if x == value:
            return True
    return False

def is_member2(value, list):
    x = 0
    while x < len(list):
        if value == list[x]:
            return True
        x += 1
    return False

def overlapping(list1, list2):
    i, j = 0, 0
    while i < len(list1):
        while j < len(list2):
            if list1[j] == list2[i]:
                return True
            j += 1
        i += 1
        j = 0
    return False

def overlapping1(list1, list2):
    for x in list1:
        for y in list2:
            if x == y:
                return True
    return False

def generate_n_characters(c,n):
    anwser = ''
    for x in range(0,n):
        anwser += c
    return anwser

def histogram(data):
    empty = ''
    for x in data:
        empty += generate_n_characters("*",x) + '\n'
    return empty

def max_in_list(numbers):
    highest = 0
    for number in numbers:
        if number > highest: highest = number
    return highest

def str_len_list(words):
    size = []
    for word in words:
        size.append(len(word))
    return size

def is_phrase_palindrome(phrase):
    to_replace = r".,!?;:()-' "
    new_word = ''
    for letter in phrase.lower():
        if letter not in to_replace:
            new_word +=letter
    if new_word == new_word[::-1]: return True
    else: return False

def panagram(sentence):
    sentence = sentence.lower() + " "
    for letter in string.ascii_lowercase + " ":
        if letter in sentence:
            continue
        else:
            return False
    return True

def panagram1(sentence):
    sentence = sentence.lower() + " "
    for letter in range(ord('a'),ord('z')+1):
        if chr(letter) in sentence:
            continue
        else:
            return True
    return True

#JUTRO TO OBCZAIĆ BO JAK NIE TO CHUJ
#/MASTĘPNY DZIEŃ/ ROZUMIEM!
def pangram2(sentence):
    char = ''
    return all(char in sentence for char in 'abcdefghijklmnopqrstuvwxyz')


def bottles_of_bear():
    for num in range(1,100):
        print("""{0} bottles of beer on the wall, {1} bootles of beer
              Take one down, pass it around, {2} bottles of beer on the wall""".format(100 - num, 100 - num, 99 - num))
    return True

def translate(words):
    y = []
    found = False
    dictionary = {"merry":"god", "christmas":"jul", "and":"och", "happy":"gott", "new":"nytt", "year":"ar"}
    for index, word in enumerate(words):
        for english, swedish in dictionary.items():
            if word == english:
                words[index] = swedish
                continue
    return words

#NO TUTAJ DAŁM POPIS XD
def translate1(words):
    dictionary = {"merry": "god", "christmas": "jul", "and": "och", "happy": "gott", "new": "nytt", "year": "ar"}
    return [swedish or word for word in words for english, swedish in dictionary.items() if word == english]

def add100(x):
    return x+100

def char_freq(sequ):
    letters = []
    freq = []
    for char in sequ:
        if char not in letters:
            letters.append(char)
            freq.append(1)
        else:
            freq[letters.index(char)] += 1
    a = dict(zip(letters, freq))
    return a

def caesar_cipher(coded):
    keys = {'a': 'n', 'b': 'o', 'c': 'p', 'd': 'q', 'e': 'r', 'f': 's', 'g': 't', 'h': 'u',
           'i': 'v', 'j': 'w', 'k': 'x', 'l': 'y', 'm': 'z', 'n': 'a', 'o': 'b', 'p': 'c',
           'q': 'd', 'r': 'e', 's': 'f', 't': 'g', 'u': 'h', 'v': 'i', 'w': 'j', 'x': 'k',
           'y': 'l', 'z': 'm', 'A': 'N', 'B': 'O', 'C': 'P', 'D': 'Q', 'E': 'R', 'F': 'S',
           'G': 'T', 'H': 'U', 'I': 'V', 'J': 'W', 'K': 'X', 'L': 'Y', 'M': 'Z', 'N': 'A',
           'O': 'B', 'P': 'C', 'Q': 'D', 'R': 'E', 'S': 'F', 'T': 'G', 'U': 'H', 'V': 'I',
           'W': 'J', 'X': 'K', 'Y': 'L', 'Z': 'M'}
    encoded = [y for x in coded for y in keys]
    return encoded

#lerning and testing comprehensions
def test_lc(numbers):
    return [n for n in numbers if n % 2 == 0]

def test_lc1(letters, numbers):
    return [(x,y) for x in letters for y in numbers]

def test_lc2(names, surnames):
    ziped = zip(names, surnames)
    return {name: hero for name, hero in ziped if name != "Michal"}

def test_lc3(numbers):
    my_set = set(numbers)
    return my_set

import re

def correct(sentence):
    #corrected = re.sub(r'\.[a-zA-Z]', '. ', sentence)
    corrected = sentence.replace('.','. ')
    corrected = re.sub(r'[\s]{2,}'," ",corrected)
    return corrected

def make_3sg_form(list_of_words):
    formated = []
    add_es = ["o", "ch", "s", "sh", "x", "z"]
    for word in list_of_words:
        if word.endswith("y"):
            print('Adding ies to', word)
            word = word[:-1] + "ies"
        elif any(ending for ending in add_es if word.endswith(ending) == True):
            word += "es"
        else:
            word += "s"
        formated.append(word)
    return formated

def make_ing_form(werbs):
    cvc = re.compile(r'[BCDFGHJKLMNPQRSTVWXYZ][aeyiou][BCDFGHJKLMNPQRSTVWXYZ]', re.I)
    exceptions = ['be', 'see', 'flee', 'knee']
    anwsers = []

    for werb in werbs:
        if werb.endswith('ie'):
            formed = werb[:-2] + 'ying'
        elif werb.endswith('e') and werb not in exceptions:
            formed = werb[:-1] + 'ing'
        elif cvc.search(werb):
            formed = werb + werb[-1] + "ing"
        else:
            formed = werb + "ing"
        anwsers.append(formed)
    return anwsers


from functools import reduce
def max_in_list_reduce(list):
    return reduce((lambda x, y: max(x,y)),list)

def string_lenght_for(words):
    numbers = []
    for word in words:
        numbers.append(len(word))
    return numbers

def string_lenght_map(words):
    return list(map(lambda x: len(x),words))

def string_lenght_list(words):
    return [len(word) for word in words]

def filter_longer_words(words, n):
    return list(filter(lambda x: len(x) > n, words))

def translate1(words):
    translations = {"merry":"god", "christmas":"jul", "and":"och", "happy":"gott", "new":"nytt", "year":"år"}
    return list(map((lambda word: translations[word] if word in translations.keys() else word), words))

def my_map(function, iterable):
    return [function(x) for x in iterable]

def my_filter(function, iterable):
    return [x for x in iterable if function(x)]

def my_reduce(function, iterable):
    x = iterable[0]
    for index, num in enumerate(iterable):
        x = function(x, num)
    return x

if __name__ == "__main__":
    print(len('siema'))
    print(sum([5,5,5]))
    print(multiply([5,5,5]))
    print(isVovel(''))
    print(translate("This is fun"))
    print(reverse("I am testing"))
    print(reverse1("I am testing"))
    print(reverse2("radar"), "radar")
    print("is Palindrome:", is_palindrome("ra31ar"))
    print("Is memeber:", is_member2(12,[1,2,3,4]))
    print("Is overlapping:", overlapping([1,2,3],[8,2,30]))
    print("Is overlapping1:", overlapping1([1,2,3],[8,2,30]))
    print("Generating n characters:", generate_n_characters("n",10))
    print("Generating histogram:\n", histogram([4,9,7]))
    print("Highest number in list:", max_in_list([1,2,3,6,54,3,65]))
    print("Length of words are:", str_len_list(["hello", "im","gay"]))
    print("Is Go hang a salami I'm a lasagna hog.?:", is_phrase_palindrome("Go hang a salami I'm a lasagna hog."))
    print("Thoes this sentence is panagram?:", panagram("The quick brown fox jumps over the lazy dog"))
    print("Thoes this sentence is panagram?1:", panagram1("The quick brown fox jumps over the lazy dog"))
    print("Thoes this sentence is panagram?2:", pangram2("the quick brown fox jumps over the lazy dog"))
    print("The song is:",bottles_of_bear())
    print("The greeting Merry christmas and happy new year in swedish is:", translate(["merry","merry", "christmas", "and", "happy", "new", "year"]))
    print("The greeting Merry christmas and happy new year in swedish is:", translate1(["merry",'merry', "christmas", "and", "happy", "new", "year"]))
    #print("Testing map", list(map(add100,[1,2,3])))
    print("Testing frequency of chars in abbabcbdbabdbdbabababcbcbab:", char_freq("abbabcbdbabdbdbabababcbcbab"))
    print("Pnrfne pvcure? V zhpu cersre Pnrfne fnynq! In Caesar cipser it means:", caesar_cipher(" Pnrfne pvcure? V zhpu cersre Pnrfne fnynq!"))
    print("Testing list comprasensions:",test_lc([1,2,3,4,5,6,7,8,9,10]))
    print("Testing Tuple comprasensions1:",test_lc1(['a', 'b', 'c', 'd'],[1,2,3,4]))
    print("Testing Dictionary comprasensions2:",test_lc2(['Andrzej', 'Michal', 'Beata', 'Daniel'],["Bisewski","Gurczynski","Szydlo","Leska"]))
    print("Testing Set comprasensions3:",test_lc3([1,1,2,3,4,5,6,7,8,9,10]))
    print("Testing correct funcion:", correct("This   is  very funny  and    cool.Indeed!"))
    print("Testing funcion making third person singular verbs:",make_3sg_form(["try", "brush", "run", "fix"]))
    print("Testing funcion making ing forms:",make_ing_form(["lie", "see", "move", "hug"]))
    print("Testing max in list using reduce():", max_in_list_reduce([1,2,3,4,5,4,3,2,1]))
    print("From words to its lenght using for-loop:", string_lenght_for(['moja', 'mama', 'orangutan', 'he']))
    print("From words to its lenght using map function:", string_lenght_map(['moja', 'mama', 'orangutan', 'he']))
    print("From words to its lenght using list comprehensions", string_lenght_list(['moja', 'mama', 'orangutan', 'he']))
    print("Returning words that are longer than 4:", filter_longer_words('moja mama orangutan piecze pali i szuka'.split(),5))
    print("Testing translate1 function using map:", translate1("merry christmas my friend and happy new year".split()))
    print("Testing my own map funcion:", my_map(lambda x: x*x, [1,2,3,4,5]))
    print("Testing my own filter funcion", my_filter((lambda x: x > 2), [1, 2, 3, 4]))
    print("Testing my own reduce funcion", my_reduce((max),[1,2,3,4,5,4]))


