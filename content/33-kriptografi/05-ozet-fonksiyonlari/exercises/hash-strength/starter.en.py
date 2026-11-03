def hash_strength(name):
    # lower-case first
    return "unknown"

for name in ["md5", "SHA1", "sha256", "blake2b", "rot13"]:
    print(name, hash_strength(name))
