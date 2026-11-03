def find_weak(lines):
    found = []
    for number, line in enumerate(lines, 1):
        if "random" in line:
            found.append(number)
    return found

code = [
    "import random",
    "import secrets",
    "pin = random.randint(1000, 9999)",
    "# random.seed(1) is only for tests",
    "key = os.urandom(32)",
    "rng = random.SystemRandom()",
    "from random import choice",
]
print(find_weak(code))
