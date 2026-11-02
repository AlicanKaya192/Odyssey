def chi_square(observed, expected):
    total = 0
    for o, e in zip(observed, expected):
        total += (o - e) ** 2 / o
    return round(total, 3)


print(chi_square([182, 174, 195, 172, 217, 216, 244], [200] * 7))
print(chi_square([30, 50, 20], [40, 40, 20]))
