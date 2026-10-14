import hashlib


def sha256_text(text):
    return hashlib.sha256(text.encode()).hexdigest()


def check_files(manifest, files):
    # First the files in the manifest, then the extra ones.
    pass


manifest = {
    "app.py": sha256_text("print('hello')"),
    "config.json": sha256_text("{}"),
    "data.csv": sha256_text("a,b"),
}
files = {"app.py": "print('hello')", "config.json": "{ }", "notes.txt": "todo"}
for line in check_files(manifest, files):
    print(line)
