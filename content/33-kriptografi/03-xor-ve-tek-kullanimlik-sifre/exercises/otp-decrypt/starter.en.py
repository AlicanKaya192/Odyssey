def otp_decrypt(cipher_hex, key_hex):
    data = bytes.fromhex(cipher_hex)
    key = bytes.fromhex(key_hex)
    return bytes(d ^ k for d, k in zip(data, key))

print(otp_decrypt("6ad09d5e491260d699234e", "3a91c47e0b5d22f6a8137e"))
print(otp_decrypt("b7b6", "ffff"))
print(otp_decrypt("6ad09d5e491260d699234e", "3a91"))
