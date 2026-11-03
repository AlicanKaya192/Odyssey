def decrypt_text(c, d, n, length):
    m = pow(c, d, n)
    data = m.to_bytes(length, "big")
    return data.decode()

n = 104723 * 104729
d = 10195862609
print(decrypt_text(5417817155, d, n, 3))
print(decrypt_text(1037036393, d, n, 2))
