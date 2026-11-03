def pad(data_hex, block):
    data = bytes.fromhex(data_hex)
    need = block - (len(data) % block)
    return (data + bytes([need]) * need).hex()


def unpad(data_hex):
    data = bytes.fromhex(data_hex)
    return data[:-data[-1]].hex()

print(unpad(pad("73686f7274", 16)) == "73686f7274")
print(unpad(pad("30313233343536373839616263646566", 16)) == "30313233343536373839616263646566")
print(unpad("030303"))
