UNITS = [
    ("years", 31536000), ("days", 86400), ("hours", 3600),
    ("minutes", 60), ("seconds", 1),
]


def crack_time(bits, guesses_per_second):
    seconds = 2 ** (bits - 1) / guesses_per_second
    # uygun birimi bul
    return (seconds, "seconds")

print(crack_time(40, 10))
print(crack_time(40, 1e10))
print(crack_time(28, 1000))
print(crack_time(10, 1e6))
