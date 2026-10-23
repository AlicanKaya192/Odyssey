import sys
from datetime import date

import inflect

p = inflect.engine()


def main():
    birth = input("Date of Birth: ")
    try:
        minutes = minutes_between(birth, date.today().isoformat())
    except ValueError:
        sys.exit("Invalid date")
    print(sing(minutes))


def minutes_between(birth, today):
    days = (date.fromisoformat(today) - date.fromisoformat(birth)).days
    return days * 24 * 60


def sing(minutes):
    words = p.number_to_words(minutes, andword="")
    return words.capitalize() + " minutes"


if __name__ == "__main__":
    main()
