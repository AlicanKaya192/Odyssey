scores = [90, 40, 75, 30, 65]
names = ["ada", "alan", "grace"]

doubled = [score * 2 for score in scores]
passed = [score for score in scores if score >= 50]
upper_names = [name.upper() for name in names]
short_names = [name.upper() for name in names if len(name) < 5]

print(doubled)
print(passed)
print(upper_names)
print(short_names)
