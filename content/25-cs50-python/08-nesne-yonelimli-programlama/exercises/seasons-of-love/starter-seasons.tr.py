import sys
from datetime import date

import inflect

p = inflect.engine()


def main():
    # Doğum tarihini al, bugünle aradaki dakikayı yazıyla yaz; geçersizse sys.exit
    ...


def minutes_between(birth, today):
    # İki YYYY-MM-DD tarihi arasındaki dakika; geçersizse ValueError
    ...


def sing(minutes):
    # Dakikayı yazıyla: büyük harfle başlar, sonunda minutes
    ...


if __name__ == "__main__":
    main()
