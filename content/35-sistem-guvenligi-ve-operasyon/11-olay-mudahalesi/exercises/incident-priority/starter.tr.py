def priority(impact, urgency):
    score = impact * urgency
    if score >= 6:
        return "P1"
    return "P3"

print(priority(3, 3))
print(priority(3, 2))
print(priority(2, 2))
print(priority(1, 2))
print(priority(4, 1))
