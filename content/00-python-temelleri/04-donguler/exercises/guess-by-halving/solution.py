secret = 371
low = 1
high = 1000
guesses = 0

while low <= high:
    guess = (low + high) // 2
    guesses = guesses + 1
    if guess > secret:
        print(f"Guess {guesses}: {guess} -> too high")
        high = guess - 1
    elif guess < secret:
        print(f"Guess {guesses}: {guess} -> too low")
        low = guess + 1
    else:
        print(f"Guess {guesses}: {guess} -> correct")
        break

print("Found", secret, "in", guesses, "guesses")
