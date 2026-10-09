import re


def valid_time(text):
    if not re.fullmatch(r"\d{2}:\d{2}", text):
        return False
    hour, minute = int(text[:2]), int(text[3:])
    return hour < 24 and minute < 60

for text in ["09:30", "23:59", "24:00", "7:15", "12:60"]:
    print(text, valid_time(text))
