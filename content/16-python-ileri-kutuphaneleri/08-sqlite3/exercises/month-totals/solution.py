import sqlite3

QUERY = ("SELECT strftime('%m', day), SUM(total) FROM orders "
         "WHERE strftime('%Y', day) = ? GROUP BY 1 ORDER BY 1")


def month_totals(orders, year):
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE orders (day TEXT, total REAL)")
    conn.executemany("INSERT INTO orders VALUES (?, ?)", orders)
    return dict(conn.execute(QUERY, (year,)))

orders = [["2026-01-05", 10.0], ["2026-01-20", 5.5], ["2026-03-02", 20.0],
          ["2025-03-10", 99.0]]
print(month_totals(orders, "2026"))
