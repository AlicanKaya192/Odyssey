import sys
from datetime import date

import inflect

p = inflect.engine()


def main():
    # Get the date of birth, print the minutes until today in words; sys.exit if invalid
    ...


def minutes_between(birth, today):
    # Minutes between two YYYY-MM-DD dates; ValueError if invalid
    ...


def sing(minutes):
    # The minutes in words: capitalized, ending in minutes
    ...


if __name__ == "__main__":
    main()
