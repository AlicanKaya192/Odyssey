import hashlib


def digest_bits(names):
    result = []
    for name in names:
        h = hashlib.new(name, b"")
        result.append([name, h.digest_size])
    return result

for name, bits in digest_bits(["md5", "sha1", "sha256", "sha512"]):
    print(name, bits)
