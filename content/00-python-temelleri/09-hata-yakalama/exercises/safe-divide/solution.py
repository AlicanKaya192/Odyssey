total = 100
numbers = [10, 5, 0, 4]

for number in numbers:
    try:
        print(total / number)
    except ZeroDivisionError:
        print("undefined")
