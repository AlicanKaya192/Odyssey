from datetime import datetime, timezone

stamps = [1710000000, 1710003600123, 1710009000, 1710012345000]

events = []
for stamp in stamps:
    seconds = stamp / 1000 if stamp > 1e12 else stamp
    events.append(datetime.fromtimestamp(seconds, tz=timezone.utc))

for event in events:
    print(event.strftime("%Y-%m-%d %H:%M:%S"))

print(round((events[-1] - events[0]).total_seconds() / 60, 1))
