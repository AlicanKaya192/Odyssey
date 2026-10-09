def index_of_smallest(numbers):
    if not numbers:
        return -1
    best = 0
    for i in range(1, len(numbers)):
        if numbers[i] < numbers[best]:
            best = i
    return best


print(index_of_smallest([5, 3, 8, 3]))
print(index_of_smallest([]))
