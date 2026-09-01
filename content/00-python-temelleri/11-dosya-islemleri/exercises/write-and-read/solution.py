with open("names.txt", "w", encoding="utf-8") as file:
    file.write("Ada\n")
    file.write("Alan\n")
    file.write("Grace\n")


with open("names.txt", encoding="utf-8") as file:
    names = file.read().splitlines()


print(len(names))
print(names)
