import hashlib


def file_report(files, known):
    lines = []
    for name in sorted(files):
        digest = hashlib.sha256(files[name].encode()).hexdigest()
        if name not in known:
            lines.append(name + " unknown")
        elif digest == known[name]:
            lines.append(name + " ok")
        else:
            lines.append(name + " changed")
    return lines

known = {
    "a.txt": "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb",
    "b.txt": "3e23e8160039594a33894f6564e1b1348bbd7a0088d42c4acb73eeaed59c009d",
}
files = {"a.txt": "a", "b.txt": "X", "c.txt": "c"}
for line in file_report(files, known):
    print(line)
