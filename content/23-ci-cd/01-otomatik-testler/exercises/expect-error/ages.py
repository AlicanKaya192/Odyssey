def parse_age(text):
    age = int(text)
    if age < 0 or age > 150:
        raise ValueError("age out of range")
    return age
