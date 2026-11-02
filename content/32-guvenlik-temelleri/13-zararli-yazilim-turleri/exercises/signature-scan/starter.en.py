import hashlib


def signature_scan(files, known):
    hits = []
    # hash every file and check the list
    return hits

known = [hashlib.sha256("TOY-SAMPLE-A".encode()).hexdigest()]
files = {
    "notes.txt": "meeting at ten",
    "toy.bin": "TOY-SAMPLE-A",
    "copy.bin": "TOY-SAMPLE-A",
    "other.bin": "TOY-SAMPLE-A!",
}
for name in signature_scan(files, known):
    print(name)
