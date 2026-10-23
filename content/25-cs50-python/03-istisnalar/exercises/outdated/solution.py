months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

while True:
    date = input("Date: ").strip()
    try:
        if "/" in date:
            month, day, year = date.split("/")
            month = int(month)
        else:
            name, day, year = date.split(" ")
            if not day.endswith(","):
                continue
            day = day.removesuffix(",")
            month = months.index(name) + 1
        day = int(day)
        year = int(year)
    except ValueError:
        continue
    if 1 <= month <= 12 and 1 <= day <= 31:
        break

print(f"{year}-{month:02}-{day:02}")
