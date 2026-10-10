import hashlib


def fingerprint(text):
    return hashlib.sha256(text).hexdigest()[:12]

print(fingerprint("hello"))
print(fingerprint("hello."))
