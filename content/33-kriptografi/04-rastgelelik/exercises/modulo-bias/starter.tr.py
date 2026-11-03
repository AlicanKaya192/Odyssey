def bias(n):
    # her sonucu say
    return [256 // n, 256 // n]

for n in [100, 16, 6]:
    print(n, bias(n))
