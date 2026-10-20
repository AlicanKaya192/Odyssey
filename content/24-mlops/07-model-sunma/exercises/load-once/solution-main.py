from store import read_model, reads

_model = None


def get_model():
    global _model
    if _model is None:
        _model = read_model()
    return _model


for request in range(5):
    model = get_model()
print("reads:", reads["count"])
print("same object:", get_model() is get_model())
print("version:", get_model()["version"])
