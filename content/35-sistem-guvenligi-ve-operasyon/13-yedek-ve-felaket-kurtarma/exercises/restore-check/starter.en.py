import hashlib


def restore_check(original, restored):
    lines = []
    for name in original:
        if original[name] == restored[name]:
            lines.append(name + ": ok")
    return lines

ORIGINAL = {"orders.csv": "1,ada", "users.csv": "ada", "keys.txt": "k1"}
RESTORED = {"orders.csv": "1,ada", "users.csv": "ad", "tmp.log": "x"}
for line in restore_check(ORIGINAL, RESTORED):
    print(line)
