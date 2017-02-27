def averange_lenght(name):
    #lets do not create another variable for storing
    av = 0
    with open(name, 'r') as f:
        for index, line in enumerate(f):
            words = [word.strip() for word in line.split()]
            av += sum(len(word) for word in words)

            number_of_words = len(words)
            if index != 0:
                number_of_words += 1
            av = av/number_of_words
    return av

file_name = input("Please enter filename:")
#file_name = 'words.txt'
print(averange_lenght(file_name))

