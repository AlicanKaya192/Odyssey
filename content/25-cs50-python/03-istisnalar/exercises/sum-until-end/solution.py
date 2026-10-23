total = 0
while True:
    try:
        line = input("Number: ")
    except EOFError:
        break
    try:
        total += int(line)
    except ValueError:
        pass
print(total)
