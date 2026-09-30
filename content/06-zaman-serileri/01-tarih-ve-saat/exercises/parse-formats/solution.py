from datetime import datetime

turkish = datetime.strptime("09.03.2024", "%d.%m.%Y")
american = datetime.strptime("12/25/2023", "%m/%d/%Y")
database = datetime.fromisoformat("2024-07-01 08:15")
email = datetime.strptime("1 February 2024", "%d %B %Y")

moments = sorted([turkish, american, database, email])
for moment in moments:
    print(moment.isoformat())
