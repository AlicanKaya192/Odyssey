def forge(cipher_hex, old, new):
    if len(old) != len(new):
        return None
    cipher = bytes.fromhex(cipher_hex)
    patch = bytes(a ^ b for a, b in zip(old.encode(), new.encode()))
    return bytes(c ^ p for c, p in zip(cipher, patch)).hex()

cipher = "6ad09d5e491260d699234e"
key = bytes.fromhex("3a91c47e0b5d22f6a8137e")
forged = forge(cipher, "PAY BOB 100", "PAY BOB 900")
print(forged)
print(bytes(c ^ k for c, k in zip(bytes.fromhex(forged), key)).decode())
print(forge(cipher, "PAY BOB 100", "PAY EVE 99999"))
