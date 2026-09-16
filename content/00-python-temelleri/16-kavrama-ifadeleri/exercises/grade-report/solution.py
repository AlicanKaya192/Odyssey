scores = {"ada": 90, "alan": 45, "grace": 72, "gauss": 38}

passed = [name for name, score in scores.items() if score >= 50]
average = sum(score for score in scores.values()) / len(scores)
lines = [
    f"{name:<8}{score:>3} " + ("ok" if score >= 50 else "no")
    for name, score in scores.items()
]

for line in lines:
    print(line)

print(f"Average: {average:.1f}")
print(f"Passed: {passed}")
