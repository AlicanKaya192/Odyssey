SIGNATURES = {"25504446": "pdf", "89504e47": "png", "504b0304": "zip"}


def file_kind(header_hex):
    return "unknown"


def mismatches(files):
    return []

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
