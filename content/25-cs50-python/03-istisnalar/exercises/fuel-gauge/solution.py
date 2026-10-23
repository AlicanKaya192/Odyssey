def main():
    percent = get_percent()
    if percent <= 1:
        print("E")
    elif percent >= 99:
        print("F")
    else:
        print(f"{percent}%")


def get_percent():
    while True:
        fraction = input("Fraction: ")
        try:
            x, y = fraction.split("/")
            x = int(x)
            y = int(y)
            ratio = x / y
        except (ValueError, ZeroDivisionError):
            continue
        if 0 <= x <= y:
            return round(ratio * 100)


main()
