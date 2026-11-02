LEVELS = ["public", "internal", "secret", "top-secret"]


def readable_objects(clearance, objects):
    names = []
    # compare every object's level
    return names

objects = {"menu": "public", "plan": "internal", "salary": "secret", "codes": "top-secret"}
print(readable_objects("internal", objects))
print(readable_objects("secret", objects))
print(readable_objects("public", {}))
