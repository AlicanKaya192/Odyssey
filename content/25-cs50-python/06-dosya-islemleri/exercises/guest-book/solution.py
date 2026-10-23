name = input("Name: ")

with open("guests.txt", "a") as file:
    file.write(f"{name}\n")
