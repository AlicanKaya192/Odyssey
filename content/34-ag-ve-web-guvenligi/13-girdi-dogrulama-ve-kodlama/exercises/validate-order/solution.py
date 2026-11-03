import re

COLORS = {"red", "green", "blue"}


def validate(form):
    errors = []
    if not re.fullmatch(r"[0-9]{5}", form.get("zip", "")):
        errors.append("zip")
    qty = form.get("qty", "")
    if not re.fullmatch(r"[0-9]{1,2}", qty) or not 1 <= int(qty) <= 99:
        errors.append("qty")
    if form.get("color") not in COLORS:
        errors.append("color")
    return errors

print(validate({"zip": "34000", "qty": "2", "color": "red"}))
print(validate({"zip": "3400", "qty": "0", "color": "pink"}))
print(validate({"qty": "99", "color": "blue"}))
