def forge(cipher_hex, old, new):
    cipher = bytes.fromhex(cipher_hex)
    # compute the patch and apply it
    return cipher_hex

cipher = "6ad09d5e491260d699234e"
key = bytes.fromhex("3a91c47e0b5d22f6a8137e")
forged = forge(cipher, "PAY BOB 100", "PAY BOB 900")
print(forged)
print(bytes(c ^ k for c, k in zip(bytes.fromhex(forged), key)).decode())
print(forge(cipher, "PAY BOB 100", "PAY EVE 99999"))
