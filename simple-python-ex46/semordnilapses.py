#im going to import words form file, not list

file_name = input("Please enter filename:")
#file_name = 'words.txt'

pointer = 0
with open(file_name) as f:
    num_lines = sum(1 for line in f)
    f.seek(0, 0)
    for x_index, x in enumerate(f):
        x = x.strip()
        #print('Checking new word:',x)
        f.seek(0, 0)
        for y_index, y in enumerate(f):
            y = y.strip()
            #print('Is',x,'and',y,'the same?')
            #check if its a polindrome and if its not the same word
            if x == y[::-1] and y_index != x_index:
                #print('Yes it is!\n\n')
                print(x,y)
            else:
                pass
                #print("No it isn't\n\n")
        pointer += len(x) + 1
        f.seek(pointer)


