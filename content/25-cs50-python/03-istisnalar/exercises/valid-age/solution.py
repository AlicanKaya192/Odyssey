def main():
    age = get_age()
    print(f"In 10 years you will be {age + 10}")


def get_age():
    while True:
        try:
            age = int(input("Age: "))
        except ValueError:
            continue
        if 0 <= age <= 120:
            return age


main()
