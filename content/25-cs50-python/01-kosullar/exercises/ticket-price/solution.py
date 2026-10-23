age = int(input("Age: "))
if age < 6:
    print("free")
elif age < 18:
    print("$5")
elif age < 65:
    print("$10")
else:
    print("$7")
