import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")
conn.execute("CREATE TABLE posts (author TEXT, title TEXT)")
conn.executemany("INSERT INTO users VALUES (?, ?)", [(1, "ada"), (2, "O'Brien")])
conn.executemany("INSERT INTO posts VALUES (?, ?)",
                 [("ada", "hello"), ("O'Brien", "notes"), ("O'Brien", "ideas")])


def report(user_id):
    row = conn.execute("SELECT name FROM users WHERE id = ?", (user_id,)).fetchone()
    if row is None:
        return []
    name = row[0]
    rows = conn.execute(f"SELECT title FROM posts WHERE author = '{name}'")
    return [r[0] for r in rows]

print(report(1))
print(report(2))
print(report(3))
