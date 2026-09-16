words = ["Ada", "alan", "Grace", "ada", "Gauss"]

initials = {word[0].lower() for word in words}
unique = {word.lower() for word in words}

print(sorted(initials))
print(sorted(unique))
