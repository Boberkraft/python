def num_files(name):
    with open(name) as f, open("Numerated "+ name, 'w') as nf:
            for index, line in enumerate(f):
                nf.write(str(index + 1) + ". " + line)

file_name = input("Please enter filename:")
#file_name = 'words.txt'

num_files(file_name)


