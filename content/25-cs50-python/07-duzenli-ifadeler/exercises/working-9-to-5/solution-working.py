import re


def main():
    print(convert(input("Hours: ")))


def convert(s):
    matches = re.fullmatch(r"(\d{1,2})(?::(\d{2}))? (AM|PM) to (\d{1,2})(?::(\d{2}))? (AM|PM)", s)
    if not matches:
        raise ValueError
    start = to_24(matches.group(1), matches.group(2), matches.group(3))
    end = to_24(matches.group(4), matches.group(5), matches.group(6))
    return f"{start} to {end}"


def to_24(hour, minute, meridiem):
    hour = int(hour)
    minute = int(minute or 0)
    if not 1 <= hour <= 12 or minute > 59:
        raise ValueError
    if meridiem == "AM":
        hour = 0 if hour == 12 else hour
    else:
        hour = 12 if hour == 12 else hour + 12
    return f"{hour:02}:{minute:02}"


if __name__ == "__main__":
    main()
