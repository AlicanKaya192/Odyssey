def otp_encrypt(message, key_hex):
    data = message.encode()
    key = bytes.fromhex(key_hex)
    return bytes(d ^ k for d, k in zip(data, key)).hex()

print(otp_encrypt("PAY BOB 100", "3a91c47e0b5d22f6a8137e"))
print(otp_encrypt("HI", "ffff"))
print(otp_encrypt("PAY BOB 100", "3a91"))
