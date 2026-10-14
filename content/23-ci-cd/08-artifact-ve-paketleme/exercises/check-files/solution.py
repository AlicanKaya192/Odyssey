import hashlib


def sha256_text(text):
    return hashlib.sha256(text.encode()).hexdigest()


def check_files(manifest, files):
    lines = []
    for name, digest in manifest.items():
        if name not in files:
            lines.append(name + ": missing")
        elif sha256_text(files[name]) != digest:
            lines.append(name + ": changed")
        else:
            lines.append(name + ": ok")
    for name in files:
        if name not in manifest:
            lines.append(name + ": unexpected")
    return lines


manifest = {
    "app.py": sha256_text("print('hello')"),
    "config.json": sha256_text("{}"),
    "data.csv": sha256_text("a,b"),
}
files = {"app.py": "print('hello')", "config.json": "{ }", "notes.txt": "todo"}
for line in check_files(manifest, files):
    print(line)
