def dh_shared(their_public, my_secret, p):
    return pow(their_public, my_secret, p)

print(dh_shared(19, 6, 23))
print(dh_shared(1, 6, 23))
print(dh_shared(22, 6, 23))
