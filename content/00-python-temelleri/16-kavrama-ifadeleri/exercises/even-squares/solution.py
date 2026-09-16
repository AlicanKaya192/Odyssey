numbers = [1, 2, 3, 4, 5, 6]

squares = [number * number for number in numbers if number % 2 == 0]
labels = ["even" if number % 2 == 0 else "odd" for number in numbers]

print(squares)
print(labels)
