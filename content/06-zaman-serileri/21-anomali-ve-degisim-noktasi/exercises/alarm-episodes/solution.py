import pandas as pd

v = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)["visits"]
past = pd.concat([v.shift(7 * k) for k in (1, 2, 3, 4)], axis=1)
deviation = v / past.median(axis=1) - 1
alarm = deviation.abs() > 0.25

days = alarm[alarm].index

episodes = []
current = [days[0]]
for day in days[1:]:
    if (day - current[-1]).days <= 3:
        current.append(day)
    else:
        episodes.append(current)
        current = [day]
episodes.append(current)

for episode in episodes:
    values = deviation.loc[episode]
    if (values > 0).all():
        direction = "up"
    elif (values < 0).all():
        direction = "down"
    else:
        direction = "mixed"
    kind = "shift" if len(episode) >= 3 else "spike"
    print(episode[0].strftime("%m-%d"), episode[-1].strftime("%m-%d"), len(episode),
          direction, kind)
