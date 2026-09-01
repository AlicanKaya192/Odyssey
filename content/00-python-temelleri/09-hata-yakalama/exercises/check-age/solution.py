def check_age(age):
    if age < 0:
        raise ValueError("age cannot be negative")
    return age


for value in [25, -3, 40]:
    try:
        print(check_age(value))
    except ValueError as error:
        print(error)
