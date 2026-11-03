def is_weak_hash(name):
    return name == "md5"

for name in ["md5", "SHA1", "sha256", "MD5"]:
    print(name, is_weak_hash(name))
