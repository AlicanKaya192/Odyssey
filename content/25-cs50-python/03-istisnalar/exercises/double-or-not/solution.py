try:
    n = int(input("Number: "))
except ValueError:
    print("Not a number")
else:
    print(n * 2)
