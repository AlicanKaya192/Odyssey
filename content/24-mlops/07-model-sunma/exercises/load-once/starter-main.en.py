from store import read_model, reads

_model = None


def get_model():
    # For now it reads the disk on every call; make it read only once.
    return read_model()


for request in range(5):
    model = get_model()
print("reads:", reads["count"])
print("same object:", get_model() is get_model())
print("version:", get_model()["version"])
