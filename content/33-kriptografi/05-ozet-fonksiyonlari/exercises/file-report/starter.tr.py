import hashlib


def file_report(files, known):
    lines = []
    for name, data in files.items():
        digest = hashlib.sha256(data.encode()).hexdigest()
        if digest == known[name]:
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
