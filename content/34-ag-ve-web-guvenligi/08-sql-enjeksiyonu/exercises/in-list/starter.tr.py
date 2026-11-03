import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (name TEXT, city TEXT)")
conn.executemany("INSERT INTO users VALUES (?, ?)",
                 [("Ada", "Izmir"), ("Bob", "L'Aquila"), ("Cem", "Izmir"),
                  ("Dan", "Oslo")])


def count_in(cities):
    names = ", ".join("'" + c + "'" for c in cities)
    row = conn.execute(f"SELECT COUNT(*) FROM users WHERE city IN ({names})").fetchone()
    return row[0]

print(count_in(["Izmir"]))
print(count_in(["Izmir", "L'Aquila"]))
print(count_in(["Paris"]))
print(count_in([]))
