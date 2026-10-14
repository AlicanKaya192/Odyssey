def missed_lines(ran, body):
    # The lines in body that are not in ran.
    pass


def coverage_percent(ran, body):
    # 100 for an empty body; otherwise the percentage of lines that ran.
    pass


print(missed_lines([2, 4, 5, 7], [2, 3, 4, 5, 6, 7]))
print(coverage_percent([2, 4, 5, 7], [2, 3, 4, 5, 6, 7]))
print(coverage_percent([1, 2, 3], [1, 2, 3]))
print(coverage_percent([], []))
