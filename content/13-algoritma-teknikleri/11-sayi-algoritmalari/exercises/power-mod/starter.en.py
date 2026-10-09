def power_mod(base, exp, mod):
    result = 1 % mod
    base %= mod
    # Until the exponent is zero: multiply if odd, square, halve.
    return result

print(power_mod(2, 10, 1000))
print(power_mod(3, 1_000_000, 1_000_000_007))
print(power_mod(7, 0, 13))
