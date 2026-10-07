import os
import sqlite3

path = os.environ.get("DB_PATH", "app.db")
con = sqlite3.connect(path)
con.execute("CREATE TABLE IF NOT EXISTS visits (id INTEGER PRIMARY KEY)")
con.execute("INSERT INTO visits DEFAULT VALUES")
con.commit()
total = con.execute("SELECT COUNT(*) FROM visits").fetchone()[0]
print("db:", path, "visits:", total)
