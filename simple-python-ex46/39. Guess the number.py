from random import randint
print("Hello! Whats is your in league of legends?")
input()
print("Well, Challenger, I am thinking of a number between 1 and 20.")
number = randint(1,20)
fails = 1
while 1:
    print('Take a guess.')
    guess = int(input())
    if guess == number:
        print("Good job, Challenger! You guessed my number ", end = '')
        if guess == 0:
            print('on first try!')
        else:
            print('in', fails,'guesses!')
        break
    else:
        fails += 1
        if guess > number:
            print('Your guess is to high.')
        else:
            print('Your guess is to low.')



