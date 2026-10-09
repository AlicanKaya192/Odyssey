def is_sorted(numbers):
    for i in range(len(numbers) - 1):
        if numbers[i] > numbers[i + 1]:
            return False
    return True


print(is_sorted([1, 2, 2, 5]))
print(is_sorted([3, 1, 2]))
print(is_sorted([]))
