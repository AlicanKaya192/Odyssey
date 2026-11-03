def ip_to_int(text):
    value = 0
    for part in text.split("."):
        value = value * 256 + int(part)
    return value

print(ip_to_int("192.168.1.10"))
print(ip_to_int("10.0.0.1"))
print(ip_to_int("255.255.255.255"))
