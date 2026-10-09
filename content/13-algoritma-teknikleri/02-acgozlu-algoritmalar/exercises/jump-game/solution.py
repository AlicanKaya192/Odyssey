def can_reach_end(jumps):
    farthest = 0
    for i, jump in enumerate(jumps):
        if i > farthest:
            return False
        farthest = max(farthest, i + jump)
    return True


print(can_reach_end([2, 3, 1, 1, 4]))
print(can_reach_end([3, 2, 1, 0, 4]))
big = [(i * 37) % 5000 for i in range(1, 300_001)]
print(can_reach_end(big))
