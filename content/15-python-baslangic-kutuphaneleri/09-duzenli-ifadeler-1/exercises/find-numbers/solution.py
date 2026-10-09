import re


def find_numbers(text):
    return [int(n) for n in re.findall(r"-?\d+", text)]

print(find_numbers("Temp -5 to 12, then 30"))
print(find_numbers("no numbers"))
