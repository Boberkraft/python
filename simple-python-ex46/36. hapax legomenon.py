import codecs

def hapax(file_name):
    #is there solution requing less memory? i think there is far better way.
    #I can make a now file insted of array or
    #only save position of words and lenght of them to get them back
    #or something like this
    array_words = []
    freq_of_words = []

    with codecs.open(file_name, encoding='utf-8') as f:
        for line in f:
            words = line.lower().split()
            for word in words:

                word_index = array_words.index(word) if word in array_words else -1
                if word_index == -1:
                    # if that word isnt yet in array
                    array_words.append(word)
                    freq_of_words.append(1)
                else:
                    #that word is in array!
                    freq_of_words[word_index] += 1

    single_ones = []
    #calculating what words were not repeted
    for index, freq in enumerate(freq_of_words):
        if freq == 1:
            single_ones.append(array_words[index])
    return single_ones

def hapax1(file_name):
    #buffed code from https://github.com/blulub/Practice/blob/master/36.%20hapax
    word_freq = {}
    with codecs.open(file_name, encoding='utf-8') as f:
        for line in f:
            words = line.lower().strip().split()
            for word in words:
                if word in word_freq:
                    word_freq[word] += 1
                else:
                    word_freq[word] = 1
    single_ones = []
    for freq in word_freq:
        if word_freq[freq] == 1:
            single_ones.append(freq)
    return single_ones



print(hapax1("words.txt"))
