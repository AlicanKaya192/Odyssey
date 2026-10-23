def main():
    year = int(input("Year: "))
    if is_leap(year):
        print("Leap year")
    else:
        print("Not a leap year")


def is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


if __name__ == "__main__":
    main()
