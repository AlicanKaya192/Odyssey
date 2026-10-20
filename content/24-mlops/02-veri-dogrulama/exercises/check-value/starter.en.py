def check_value(value, low, high):
    # First None, then the type, then the range.
    pass


print(check_value(30, 1, 72))
print(check_value(None, 1, 72))
print(check_value("30", 1, 72))
print(check_value(0, 1, 72))
print(check_value(72, 1, 72))
