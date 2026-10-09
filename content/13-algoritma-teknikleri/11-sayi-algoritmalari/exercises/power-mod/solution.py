def power_mod(base, exp, mod):
    result = 1 % mod
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = result * base % mod
        base = base * base % mod
        exp //= 2
    return result

print(power_mod(2, 10, 1000))
print(power_mod(3, 1_000_000, 1_000_000_007))
print(power_mod(7, 0, 13))
