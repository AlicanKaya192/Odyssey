import sqlite3


def top_products(items, n):
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE products (name TEXT, price REAL)")
    # row_factory, executemany, ORDER BY price DESC LIMIT ?
    return []

items = [["pen", 1.5], ["ink", 0.5], ["book", 12.0], ["bag", 30.0]]
print(top_products(items, 2))
