def random_source(purpose):
    return "random"

for purpose in ["token", "dice", "salt", "simulation"]:
    print(purpose, random_source(purpose))
