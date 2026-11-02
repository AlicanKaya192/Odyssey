def keyspace_years(bits, rate):
    years = 2 * bits / rate / (365 * 24 * 3600)
    return f"{years:.2e}"

for bits in [40, 64, 128]:
    print(bits, keyspace_years(bits, 10**12))
