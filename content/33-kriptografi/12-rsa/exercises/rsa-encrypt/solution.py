def rsa_encrypt(m, e, n):
    if m < 0 or m >= n:
        return "too large"
    return pow(m, e, n)

print(rsa_encrypt(65, 17, 3233))
print(rsa_encrypt(3233, 17, 3233))
print(rsa_encrypt(5000, 17, 3233))
