def check_key(algorithm, bits):
    if algorithm == "rsa":
        return "ok" if bits >= 2048 else "too short"
    if algorithm == "aes":
        return "ok" if bits in [128, 192, 256] else "too short"
    if algorithm == "ec":
        return "ok" if bits >= 256 else "too short"
    return "unknown"

print(check_key("rsa", 1024))
print(check_key("aes", 64))
print(check_key("ec", 256))
print(check_key("des", 56))
