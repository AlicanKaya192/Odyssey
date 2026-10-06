class_a = {"Ada", "Alan", "Grace", "Linus", "Guido"}
class_b = {"Grace", "Guido", "Margaret", "Linus", "Dennis", "Ken"}

both = class_a & class_b
only_a = class_a - class_b
only_b = class_b - class_a
total = len(class_a | class_b)

print("Both:", sorted(both))
print("Only A:", sorted(only_a))
print("Only B:", sorted(only_b))
print("Total:", total)
