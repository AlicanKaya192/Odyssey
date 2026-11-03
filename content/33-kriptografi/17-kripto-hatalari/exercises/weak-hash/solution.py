def is_weak_hash(name):
    return name.lower() in ["md4", "md5", "sha1"]

for name in ["md5", "SHA1", "sha256", "MD5"]:
    print(name, is_weak_hash(name))
