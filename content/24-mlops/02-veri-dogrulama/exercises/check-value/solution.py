def check_value(value, low, high):
    if value is None:
        return "missing"
    if not isinstance(value, (int, float)):
        return "not a number"
    if not low <= value <= high:
        return "out of range"
    return "ok"


print(check_value(30, 1, 72))
print(check_value(None, 1, 72))
print(check_value("30", 1, 72))
print(check_value(0, 1, 72))
print(check_value(72, 1, 72))
