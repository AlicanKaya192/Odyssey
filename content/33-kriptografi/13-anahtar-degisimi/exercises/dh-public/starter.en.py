def dh_public(g, secret, p):
    return pow(secret, g, p)

print(dh_public(5, 6, 23))
print(dh_public(5, 15, 23))
