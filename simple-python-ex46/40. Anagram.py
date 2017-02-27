from random import randint, sample


words = "brown red green yellow white black".split()
word = words[randint(0, len(words))]
print(word)
anagram = ''.join(sample(word, len(word)))
print("Colour word anagram:", anagram)

while 1:
    guess = input("Guess the colour word!\n")
    if guess == word:
        print("Correct!")
        break
