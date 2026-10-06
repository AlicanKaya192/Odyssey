year = 1900

is_leap = (year % 4 == 0 and year % 100 != 0) or year % 400 == 0

print(year, "is a leap year:", is_leap)
