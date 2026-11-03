import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (name TEXT, city TEXT)")
conn.executemany("INSERT INTO users VALUES (?, ?)",
                 [("Ada", "Istanbul"), ("O'Brien", "Izmir"),
                  ('Ann "Jr" Lee', "Ankara")])


def city_of(name):
    query = "SELECT city FROM users WHERE name = '" + name + "'"
    row = conn.execute(query).fetchone()
    return row[0] if row else "unknown"

for name in ["Ada", "O'Brien", 'Ann "Jr" Lee', "Nobody"]:
    print(city_of(name))
