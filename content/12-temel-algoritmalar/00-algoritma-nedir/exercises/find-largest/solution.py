def find_largest(numbers):
    largest = numbers[0]
    for number in numbers:
        if number > largest:
            largest = number
    return largest


print(find_largest([4, 17, 9, 12]))
print(find_largest([-6, -3, -11]))
