from contextlib import contextmanager


@contextmanager
def transaction(data):
    yield data

data = {"balance": 100}
with transaction(data):
    data["balance"] -= 30
print(data)
try:
    with transaction(data):
        data["balance"] -= 500
        raise ValueError("not enough money")
except ValueError as error:
    print("ValueError:", error)
print(data)
