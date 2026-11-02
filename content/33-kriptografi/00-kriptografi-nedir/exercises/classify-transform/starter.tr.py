def classify_transform(name):
    # once ismi kucuk harfe cevir
    return "unknown"

for name in ["Base64", "sha256", "AES", "hex", "rot13"]:
    print(name, classify_transform(name))
