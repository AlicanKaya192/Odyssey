from datetime import datetime, timezone


def text_to_stamp(text):
    moment = datetime.strptime(text, "%Y-%m-%d %H:%M")
    return int(moment.timestamp())

print(text_to_stamp("2026-03-15 14:30"))
print(text_to_stamp("1970-01-02 00:00"))
