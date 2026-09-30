from datetime import datetime, timedelta

shifts = [
    ("2024-03-08 22:15", 7, 50),
    ("2024-03-09 23:40", 6, 30),
    ("2024-03-10 21:05", 9, 0),
]

total = timedelta(0)
for start_text, hours, minutes in shifts:
    start = datetime.fromisoformat(start_text)
    length = timedelta(hours=hours, minutes=minutes)
    end = start + length
    total += length
    print(end.strftime("%Y-%m-%d %H:%M"), end.strftime("%A"))

print(round(total.total_seconds() / 3600, 1))
