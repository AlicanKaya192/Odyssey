colors = ["red", "green", "blue", "yellow"]

try:
    i = int(input("Position: "))
    print(colors[i])
except ValueError:
    print("Not a number")
except IndexError:
    print("No such position")
