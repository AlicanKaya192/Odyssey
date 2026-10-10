import argparse
import sqlite3
from decimal import Decimal

ORDERS = [("ada", "19.99"), ("alan", "5.01"), ("ada", "12.50"), ("grace", "40.00")]


def report(argv):
    parser = argparse.ArgumentParser(prog="report")
    parser.add_argument("--min", type=Decimal, default=Decimal("0"))
    parser.add_argument("--customer")
    args = parser.parse_args(argv)
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, customer TEXT, total TEXT)")
    conn.executemany("INSERT INTO orders (customer, total) VALUES (?, ?)", ORDERS)
    query = "SELECT id, total FROM orders"
    params = ()
    if args.customer:
        query += " WHERE customer = ?"
        params = (args.customer,)
    rows = conn.execute(query + " ORDER BY id", params).fetchall()
    conn.close()
    return [[i, total] for i, total in rows if Decimal(total) >= args.min]

print(report(["--min", "10"]))
print(report(["--customer", "ada"]))
