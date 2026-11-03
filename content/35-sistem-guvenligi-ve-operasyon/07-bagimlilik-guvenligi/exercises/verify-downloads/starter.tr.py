import hashlib


def verify_downloads(files, lock):
    lines = []
    for name, content in files.items():
        digest = hashlib.sha256(content.encode()).hexdigest()
        if digest == lock[name]:
            lines.append(name + ": ok")
        else:
            lines.append(name + ": mismatch")
    return lines

import hashlib

LOCK = {
    "alpha-1.0.zip": hashlib.sha256(b"alpha 1.0").hexdigest(),
    "beta-2.1.zip": hashlib.sha256(b"beta 2.1").hexdigest(),
}
FILES = {
    "beta-2.1.zip": "beta 2.1 + extra",
    "alpha-1.0.zip": "alpha 1.0",
    "gamma-0.3.zip": "gamma 0.3",
}
for line in verify_downloads(FILES, LOCK):
    print(line)
