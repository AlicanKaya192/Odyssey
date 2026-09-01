with open("log.txt", "w", encoding="utf-8") as file:
    file.write("start\n")


with open("log.txt", "a", encoding="utf-8") as file:
    file.write("step one\n")


with open("log.txt", "a", encoding="utf-8") as file:
    file.write("step two\n")


with open("log.txt", encoding="utf-8") as file:
    entries = file.read().splitlines()


print(len(entries))
print(entries)
