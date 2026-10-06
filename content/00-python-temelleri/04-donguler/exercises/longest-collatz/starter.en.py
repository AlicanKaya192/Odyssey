limit = 30

best_start = 0
best_steps = 0

# Outer loop: every starting number from 1 to limit
#   n = start, steps = 0
#   Inner loop (while): apply the rule until n is 1, count the steps
#   If this journey is longer than the best so far, update best_start and best_steps


print("Longest:", best_start, "with", best_steps, "steps")
