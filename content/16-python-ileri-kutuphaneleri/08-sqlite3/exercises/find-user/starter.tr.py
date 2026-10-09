import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (name TEXT, admin INTEGER)")
conn.execute("INSERT INTO users VALUES ('ada', 1), ('alan', 0)")


def find_user(name):
    query = f"SELECT name FROM users WHERE name = '{name}'"
    return [row[0] for row in conn.execute(query)]

print(find_user("ada"))
print(find_user("x' OR '1'='1"))
