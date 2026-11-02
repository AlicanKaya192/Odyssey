import hashlib


def signature_scan(files, known):
    bad = set(known)
    hits = [name for name, content in files.items()
            if hashlib.sha256(content.encode()).hexdigest() in bad]
    return sorted(hits)

known = [hashlib.sha256("TOY-SAMPLE-A".encode()).hexdigest()]
files = {
    "notes.txt": "meeting at ten",
    "toy.bin": "TOY-SAMPLE-A",
    "copy.bin": "TOY-SAMPLE-A",
    "other.bin": "TOY-SAMPLE-A!",
}
for name in signature_scan(files, known):
    print(name)
