scores = [45, 82, 67, 30, 95, 58]

passed = []
for score in scores:
    if score >= 60:
        passed.append(score)

print(passed)
print(len(passed))
