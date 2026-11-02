def classify_transform(name):
    # lower-case the name first
    return "unknown"

for name in ["Base64", "sha256", "AES", "hex", "rot13"]:
    print(name, classify_transform(name))
