words = ["ada", "alan", "grace"]
scores = {"ada": 90, "alan": 45, "grace": 72}

lengths = {word: len(word) for word in words}
passed = {name: score for name, score in scores.items() if score >= 50}
flipped = {score: name for name, score in scores.items()}

print(lengths)
print(passed)
print(flipped)
