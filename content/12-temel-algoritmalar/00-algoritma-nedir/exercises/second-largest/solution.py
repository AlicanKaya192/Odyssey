def second_largest(numbers):
    first = None
    second = None
    for number in numbers:
        if first is None or number > first:
            second = first
            first = number
        elif number < first and (second is None or number > second):
            second = number
    return second


print(second_largest([4, 9, 7, 9]))
print(second_largest([5, 5]))
print(second_largest([-2, -8, -5]))
