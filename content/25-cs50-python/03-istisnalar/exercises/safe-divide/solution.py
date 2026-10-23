try:
    x = int(input("x: "))
    y = int(input("y: "))
    result = x / y
except ValueError:
    print("Invalid number")
except ZeroDivisionError:
    print("Cannot divide by zero")
else:
    print(f"{result:.2f}")
