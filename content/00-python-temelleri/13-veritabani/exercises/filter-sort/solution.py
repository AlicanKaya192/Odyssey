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


cursor.execute(
    "SELECT name, grade FROM students WHERE grade >= 50 ORDER BY grade DESC"
)
passing = cursor.fetchall()

cursor.execute("SELECT name FROM students WHERE city = ?", ("London",))
londoners = []
for row in cursor.fetchall():
    londoners.append(row[0])

print(passing)
print(londoners)
