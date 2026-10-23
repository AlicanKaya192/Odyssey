import random


def main():
    level = get_positive("Level: ")
    number = random.randint(1, level)
    while True:
        guess = get_positive("Guess: ")
        if guess < number:
            print("Too small!")
        elif guess > number:
            print("Too large!")
        else:
            print("Just right!")
            break


def get_positive(prompt):
    while True:
        try:
            n = int(input(prompt))
        except ValueError:
            continue
        if n > 0:
            return n


main()
