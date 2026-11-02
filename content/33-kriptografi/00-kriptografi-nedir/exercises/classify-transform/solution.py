KINDS = {
    "encoding": {"base64", "hex", "url"},
    "hashing": {"md5", "sha1", "sha256", "sha3-256"},
    "encryption": {"aes", "chacha20", "rsa"},
}


def classify_transform(name):
    name = name.lower()
    for kind, names in KINDS.items():
        if name in names:
            return kind
    return "unknown"

for name in ["Base64", "sha256", "AES", "hex", "rot13"]:
    print(name, classify_transform(name))
