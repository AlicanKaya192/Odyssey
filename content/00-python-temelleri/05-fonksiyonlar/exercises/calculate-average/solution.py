def calculate_average(numbers):
    total = 0
    count = 0
    for number in numbers:
        total = total + number
        count = count + 1
    return total / count


scores = [10, 20, 30, 40]
average = calculate_average(scores)

print(average)
