def check_key(algorithm, bits):
    if algorithm == "rsa":
        if bits >= 2048:
            return "ok"
        return "too short"
    return "ok"

print(check_key("rsa", 1024))
print(check_key("aes", 64))
print(check_key("ec", 256))
print(check_key("des", 56))
