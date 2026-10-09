import tempfile
from pathlib import Path


def temp_roundtrip(files):
    names = []
    # with tempfile.TemporaryDirectory() as tmp:
    return names, True

print(temp_roundtrip({"b.txt": "two", "a.txt": "one"}))
