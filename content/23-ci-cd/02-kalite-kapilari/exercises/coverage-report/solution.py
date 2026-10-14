def missed_lines(ran, body):
    missed = []
    for line in body:
        if line not in ran:
            missed.append(line)
    return missed


def coverage_percent(ran, body):
    if len(body) == 0:
        return 100
    covered = len(body) - len(missed_lines(ran, body))
    return round(100 * covered / len(body))


print(missed_lines([2, 4, 5, 7], [2, 3, 4, 5, 6, 7]))
print(coverage_percent([2, 4, 5, 7], [2, 3, 4, 5, 6, 7]))
print(coverage_percent([1, 2, 3], [1, 2, 3]))
print(coverage_percent([], []))
