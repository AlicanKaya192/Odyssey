import io
import pickle
from collections import Counter

ALLOWED = {("collections", "Counter")}


class SafeUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if (module, name) in ALLOWED:
            return super().find_class(module, name)
        raise pickle.UnpicklingError(f"blocked: {module}.{name}")


def load_safely(blob):
    try:
        return SafeUnpickler(io.BytesIO(blob)).load()
    except pickle.UnpicklingError as error:
        return str(error)


class Trap:
    def __reduce__(self):
        return (print, ("loaded!",))


print(load_safely(pickle.dumps(Counter("abca"))))
print(load_safely(pickle.dumps(Trap())))
print(load_safely(pickle.dumps([1, "x", None])))
