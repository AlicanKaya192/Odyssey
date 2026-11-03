import hashlib


def digest(message, n):
    h = hashlib.sha256(message.encode()).digest()
    return int.from_bytes(h, "big") % n


def parse(version):
    return [int(part) for part in version.split(".")]


def check_update(version, signature, e, n, installed):
    if pow(signature, e, n) != digest("app " + version, n):
        return "bad signature"
    if parse(version) <= parse(installed):
        return "downgrade"
    return "install"

n = 104723 * 104729
print(check_update("2.10.0", 6739506677, 65537, n, "2.9.0"))
print(check_update("2.8.0", 9900516037, 65537, n, "2.9.0"))
print(check_update("2.11.0", 6739506677, 65537, n, "2.9.0"))
