import sys

if len(sys.argv) < 2:
    sys.exit("Too few command-line arguments")
if len(sys.argv) > 2:
    sys.exit("Too many command-line arguments")
if not sys.argv[1].endswith(".py"):
    sys.exit("Not a Python file")

try:
    with open(sys.argv[1]) as file:
        lines = file.readlines()
except FileNotFoundError:
    sys.exit("File does not exist")

count = 0
for line in lines:
    code = line.lstrip()
    if code and not code.startswith("#"):
        count += 1
print(count)
