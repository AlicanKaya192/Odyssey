import sqlite3


def top_products(items, n):
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE products (name TEXT, price REAL)")
    conn.executemany("INSERT INTO products VALUES (?, ?)", items)
    query = "SELECT name FROM products ORDER BY price DESC LIMIT ?"
    return [row["name"] for row in conn.execute(query, (n,))]

items = [["pen", 1.5], ["ink", 0.5], ["book", 12.0], ["bag", 30.0]]
print(top_products(items, 2))
