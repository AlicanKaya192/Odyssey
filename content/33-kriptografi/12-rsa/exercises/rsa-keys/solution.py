def rsa_keys(p, q, e):
    n = p * q
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    return [n, d]

n, d = rsa_keys(61, 53, 17)
print(n, d)
print(17 * d % ((61 - 1) * (53 - 1)))
