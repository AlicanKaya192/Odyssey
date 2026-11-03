import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE products (name TEXT, price INTEGER)")
conn.executemany("INSERT INTO products VALUES (?, ?)",
                 [("pen", 3), ("book", 12), ("bag", 30), ("cup", 7)])
SORTABLE = {"name": "name", "price": "price"}


def sorted_names(sort):
    column = SORTABLE.get(sort, "name")
    rows = conn.execute(f"SELECT name FROM products ORDER BY {column}")
    return [r[0] for r in rows]

print(sorted_names("price"))
print(sorted_names("name"))
print(sorted_names("price DESC"))
