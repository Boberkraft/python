from collections import defaultdict

# my oryginal code was crap and did serching in about 5 minutes lol
# so i looked online and found awsome solution for this exercise
# https://github.com/R4meau/46-simple-python-exercises/blob/master/exercises/ex43.py
# i just almost did the same but with 3 temp files

def anagram_finder(filename):
    length = 0
    words = []
    with open(filename, 'r') as file:
        for word in file:
            words.append(word.rstrip())
    anagrams = defaultdict(list)

    for word in words:
        anagrams[''.join(sorted(word))].append(word)

    for anagram, words in anagrams.items():
        if len(words) > length:
            length = len(words)

    for anagram, words in anagrams.items():
        if len(words) == length:
            print(anagram, words)

anagram_finder('words.txt')