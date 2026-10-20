def directional_share(before, after, tolerance):
    if not before:
        return None
    held = sum(1 for b, a in zip(before, after) if a >= b - tolerance)
    return round(held / len(before), 3)


before = [0.10, 0.40, 0.55, 0.80]
after = [0.20, 0.39, 0.70, 0.80]
print(directional_share(before, after, 0.0))
print(directional_share(before, after, 0.02))
print(directional_share([], [], 0.0))
