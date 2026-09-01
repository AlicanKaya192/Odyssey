grades: dict[str, int] = {"Ada": 90, "Alan": 70}
passed: list[str] = []


def average(values: dict[str, int]) -> int:
    return sum(values.values()) // len(values)


for name in grades:
    if grades[name] >= 80:
        passed.append(name)


print(average(grades))
print(passed)
