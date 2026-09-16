solved = 24
total = 257

remaining = total - solved
rate = solved / total

print(f"Solved: {solved} / {total}")
print(f"Rate: {rate:.1%}")
print(f"Remaining: {remaining} ({1 - rate:.1%})")
