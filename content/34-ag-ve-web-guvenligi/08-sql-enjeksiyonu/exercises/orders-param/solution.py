import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE orders (owner TEXT, item TEXT)")
conn.executemany("INSERT INTO orders VALUES (?, ?)",
                 [("ada", "book"), ("ada", "pen"), ("O'Brien", "lamp"),
                  ("bob", "laptop")])


def orders_for(owner):
    rows = conn.execute("SELECT item FROM orders WHERE owner = ?", (owner,))
    return [r[0] for r in rows]

for owner in ["ada", "O'Brien", "x' OR '1'='1", ""]:
    print(repr(owner), orders_for(owner))
