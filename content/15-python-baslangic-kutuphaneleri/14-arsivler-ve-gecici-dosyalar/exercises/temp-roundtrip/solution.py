import tempfile
from pathlib import Path


def temp_roundtrip(files):
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        for name, text in files.items():
            (base / name).write_text(text, encoding="utf-8")
        names = sorted(p.name for p in base.iterdir())
    return names, base.exists()

print(temp_roundtrip({"b.txt": "two", "a.txt": "one"}))
