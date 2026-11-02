LEVELS = ["public", "internal", "secret", "top-secret"]


def readable_objects(clearance, objects):
    limit = LEVELS.index(clearance)
    names = [name for name, level in objects.items() if LEVELS.index(level) <= limit]
    return sorted(names)

objects = {"menu": "public", "plan": "internal", "salary": "secret", "codes": "top-secret"}
print(readable_objects("internal", objects))
print(readable_objects("secret", objects))
print(readable_objects("public", {}))
