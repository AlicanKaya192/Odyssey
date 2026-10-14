def missed_lines(ran, body):
    # body'de olup ran'da olmayanlar.
    pass


def coverage_percent(ran, body):
    # Bos body'de 100; degilse calisan satirlarin yuzdesi.
    pass


print(missed_lines([2, 4, 5, 7], [2, 3, 4, 5, 6, 7]))
print(coverage_percent([2, 4, 5, 7], [2, 3, 4, 5, 6, 7]))
print(coverage_percent([1, 2, 3], [1, 2, 3]))
print(coverage_percent([], []))
