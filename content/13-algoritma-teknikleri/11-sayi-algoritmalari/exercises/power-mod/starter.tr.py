def power_mod(base, exp, mod):
    result = 1 % mod
    base %= mod
    # Us sifir olana kadar: tekse carp, kare al, yariya bol.
    return result

print(power_mod(2, 10, 1000))
print(power_mod(3, 1_000_000, 1_000_000_007))
print(power_mod(7, 0, 13))
