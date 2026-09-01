def summarise(values):
    passed = 0
    failed = 0

    for value in values:
        if value >= 50:
            passed = passed + 1
        else:
            failed = failed + 1

    average = sum(values) // len(values)
    return passed, failed, average


high, low, mean = summarise([90, 40, 75, 30, 65])

print(high)
print(low)
print(mean)
