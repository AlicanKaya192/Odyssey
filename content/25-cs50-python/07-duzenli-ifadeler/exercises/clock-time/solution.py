import re

time = input("Time: ").strip()

if re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", time):
    print("Valid")
else:
    print("Invalid")
