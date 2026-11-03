import re

COLORS = {"red", "green", "blue"}


def validate(form):
    errors = []
    # uc alani sirayla denetle
    return errors

print(validate({"zip": "34000", "qty": "2", "color": "red"}))
print(validate({"zip": "3400", "qty": "0", "color": "pink"}))
print(validate({"qty": "99", "color": "blue"}))
