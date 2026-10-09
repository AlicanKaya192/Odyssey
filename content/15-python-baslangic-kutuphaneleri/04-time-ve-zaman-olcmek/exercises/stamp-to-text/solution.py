from datetime import datetime, timezone


def stamp_to_text(stamp):
    moment = datetime.fromtimestamp(stamp, timezone.utc)
    return moment.strftime("%Y-%m-%d %H:%M")

print(stamp_to_text(1773585000))
print(stamp_to_text(0))
