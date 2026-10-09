import sqlite3


def load_scores(rows):
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE scores (name TEXT, score INTEGER)")
    conn.executemany("INSERT INTO scores VALUES (?, ?)", rows)
    query = "SELECT COUNT(*), ROUND(AVG(score), 1) FROM scores"
    return list(conn.execute(query).fetchone())

print(load_scores([["ada", 90], ["alan", 75], ["grace", 82]]))
