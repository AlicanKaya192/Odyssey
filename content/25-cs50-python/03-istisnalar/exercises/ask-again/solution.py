while True:
    try:
        n = int(input("Number: "))
    except ValueError:
        print("Try again")
    else:
        break
print(n + 1)
