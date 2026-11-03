def pad(data_hex, block):
    data = bytes.fromhex(data_hex)
    need = block - (len(data) % block)
    if need == 0:
        return data_hex
    return (data + bytes([need]) * need).hex()

for text in ["73686f7274", "30313233343536373839616263646566"]:
    padded = pad(text, 16)
    raw = bytes.fromhex(text)
    out = bytes.fromhex(padded)
    print(len(raw), "->", len(out), "last:", out[-1])
