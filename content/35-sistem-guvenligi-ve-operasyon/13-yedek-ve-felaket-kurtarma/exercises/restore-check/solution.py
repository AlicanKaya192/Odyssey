import hashlib


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def restore_check(original, restored):
    lines = []
    for name in sorted(set(original) | set(restored)):
        if name not in original:
            lines.append(name + ": extra")
        elif name not in restored:
            lines.append(name + ": missing")
        elif digest(original[name]) == digest(restored[name]):
            lines.append(name + ": ok")
        else:
            lines.append(name + ": different")
    return lines

ORIGINAL = {"orders.csv": "1,ada", "users.csv": "ada", "keys.txt": "k1"}
RESTORED = {"orders.csv": "1,ada", "users.csv": "ad", "tmp.log": "x"}
for line in restore_check(ORIGINAL, RESTORED):
    print(line)
