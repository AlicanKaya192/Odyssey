WEAK = {"md5", "sha1"}
STRONG = {"sha256", "sha512", "sha3_256", "blake2b"}


def hash_strength(name):
    name = name.lower()
    if name in WEAK:
        return "weak"
    if name in STRONG:
        return "strong"
    return "unknown"

for name in ["md5", "SHA1", "sha256", "blake2b", "rot13"]:
    print(name, hash_strength(name))
