def escape_like(term):
    return term.replace("%", "\\%").replace("_", "\\_").replace("\\", "\\\\")

import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE notes (text TEXT)")
conn.executemany("INSERT INTO notes VALUES (?)",
                 [("50% discount",), ("500 pens",), ("plan_b",)])
for term in ["0%", "_", "n_b"]:
    pattern = "%" + escape_like(term) + "%"
    rows = conn.execute("SELECT text FROM notes WHERE text LIKE ? ESCAPE '\\'",
                        (pattern,)).fetchall()
    print(term, [r[0] for r in rows])
