limit = 30

best_start = 0
best_steps = 0

for start in range(1, limit + 1):
    n = start
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = n * 3 + 1
        steps = steps + 1
    if steps > best_steps:
        best_start = start
        best_steps = steps

print("Longest:", best_start, "with", best_steps, "steps")
