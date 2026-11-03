def priority(impact, urgency):
    if impact not in (1, 2, 3) or urgency not in (1, 2, 3):
        return "invalid"
    score = impact * urgency
    if score >= 6:
        return "P1"
    if score >= 4:
        return "P2"
    return "P3"

print(priority(3, 3))
print(priority(3, 2))
print(priority(2, 2))
print(priority(1, 2))
print(priority(4, 1))
