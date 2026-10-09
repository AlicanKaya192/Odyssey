import io
import pickle
from collections import Counter

ALLOWED = {("collections", "Counter")}


def load_safely(blob):
    return pickle.loads(blob)


class Trap:
    def __reduce__(self):
        return (print, ("loaded!",))


print(load_safely(pickle.dumps(Counter("abca"))))
print(load_safely(pickle.dumps(Trap())))
print(load_safely(pickle.dumps([1, "x", None])))
