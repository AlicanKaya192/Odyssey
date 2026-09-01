import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

cursor.execute("CREATE TABLE students (name TEXT, grade INTEGER, city TEXT)")

rows = [
    ("Ada", 90, "London"),
    ("Brian", 40, "London"),
    ("Grace", 75, "New York"),
    ("Alan", 60, "London"),
]

cursor.executemany("INSERT INTO students VALUES (?, ?, ?)", rows)
connection.commit()

cursor.execute("SELECT COUNT(*) FROM students")
total = cursor.fetchone()[0]

cursor.execute("SELECT name FROM students")
names = []
for row in cursor.fetchall():
    names.append(row[0])

print(total)
print(names)
