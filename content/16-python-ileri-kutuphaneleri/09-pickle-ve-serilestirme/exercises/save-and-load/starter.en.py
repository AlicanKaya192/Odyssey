import pickle


def save_and_load(path, obj):
    with open(path, "w") as file:
        pickle.dump(obj, file)
    with open(path, "r") as file:
        return pickle.load(file)

print(save_and_load("scores.pkl", {"ada": [90, 85]}))
