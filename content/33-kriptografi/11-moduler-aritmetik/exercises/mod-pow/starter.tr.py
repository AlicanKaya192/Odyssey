def mod_pow(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        exp >>= 1
    return result

print(mod_pow(7, 128, 13))
print(mod_pow(5, 117, 19))
print(mod_pow(2, 10, 1000))
