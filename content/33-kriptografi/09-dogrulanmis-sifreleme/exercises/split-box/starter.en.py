def split_box(box_hex):
    # nonce 8 bytes, tag 32 bytes
    tag = box_hex[:64]
    nonce = box_hex[64:80]
    cipher = box_hex[80:]
    return [nonce, cipher, tag]

box = "11" * 8 + "aabbcc" + "ee" * 32
nonce, cipher, tag = split_box(box)
print(nonce)
print(cipher)
print(len(tag) // 2, "byte tag")
