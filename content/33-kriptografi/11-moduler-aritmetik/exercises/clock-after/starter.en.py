def clock_after(hour, hours):
    result = hour + hours
    if result >= 24:
        result = result - 24
    return result

print(clock_after(22, 5))
print(clock_after(10, 50))
print(clock_after(3, -5))
