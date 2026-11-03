def clock_after(hour, hours):
    return (hour + hours) % 24

print(clock_after(22, 5))
print(clock_after(10, 50))
print(clock_after(3, -5))
