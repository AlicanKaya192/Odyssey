def hash_strength(name):
    # once kucuk harfe cevir
    return "unknown"

for name in ["md5", "SHA1", "sha256", "blake2b", "rot13"]:
    print(name, hash_strength(name))
