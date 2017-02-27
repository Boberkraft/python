test = """ Mr. Smith bought cheapsite.com for 1.5 million dollars, i.e. he paid a lot for it. Did he mind? Adam Jones Jr. thinks he didn't. In any case, this isn't true... Well, with a probability of .9 it isn't"""
words = test.split()
titles = 'Mr Mrs Dr'.split()
new = ''

max_words_index = len(words) - 1
for w_index, word in enumerate(words):
    max_letter_index = len(word) - 1
    for l_index, letter in enumerate(word):
        if letter in '. ? !'.split():
            if max_words_index - w_index >= 1:
                if words[w_index + 1][0].islower():
                    new += letter
                elif word[:-1] in titles:
                    new += letter
                elif max_letter_index == l_index:
                    new += letter + '\n'
        else:
            new += letter
        if l_index == len(word)-1 and not new.endswith('\n'):
            new += ' '
print(new)

