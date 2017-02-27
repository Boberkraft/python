def is_palindrome(sentence):
    if sentence == sentence[::-1]:
        return True
    else:
        return False

file_name = input("Please type filename:")
#the words.txt file contains words to test for being palindroms
with open(file_name) as f:
    for word in f:
        word = word.strip()
        if is_palindrome(word):
            print(word)