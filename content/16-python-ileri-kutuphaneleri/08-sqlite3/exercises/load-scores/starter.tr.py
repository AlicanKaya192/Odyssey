import sqlite3


def load_scores(rows):
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE scores (name TEXT, score INTEGER)")
    for row in rows:
        conn.execute("INSERT INTO scores VALUES (?, ?)", row)
    return []

print(load_scores([["ada", 90], ["alan", 75], ["grace", 82]]))
