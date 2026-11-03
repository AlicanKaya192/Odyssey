SIGNATURES = {"25504446": "pdf", "89504e47": "png", "504b0304": "zip"}


def file_kind(header_hex):
    header = header_hex.lower()
    for signature, kind in SIGNATURES.items():
        if header.startswith(signature):
            return kind
    return "unknown"


def mismatches(files):
    found = []
    for name, header_hex in files.items():
        kind = file_kind(header_hex)
        extension = name.rsplit(".", 1)[1]
        if kind != "unknown" and kind != extension:
            found.append(name)
    return sorted(found)

print(file_kind("25504446312e37"))
print(file_kind("504b0304"))
print(file_kind("6d656574"))
FILES = {
    "report.pdf": "255044462d31",
    "photo.png": "504b03040a00",
    "notes.txt": "6d656574696e",
    "logo.png": "89504e470d0a",
}
print(mismatches(FILES))
