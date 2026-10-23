import sys

if len(sys.argv) != 2:
    sys.exit("Usage: python cozum.py FILE")

try:
    with open(sys.argv[1]) as file:
        lines = file.readlines()
except FileNotFoundError:
    sys.exit("File does not exist")

words = 0
for line in lines:
    words += len(line.split())
print(f"{len(lines)} lines, {words} words")
