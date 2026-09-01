import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

cursor.execute("CREATE TABLE students (name TEXT, grade INTEGER, city TEXT)")

rows = [
    ("Ada", 90, "London"),
    ("Brian", 40, "London"),
    ("Grace", 75, "New York"),
    ("Alan", 60, "London"),
    ("Edith", 95, "New York"),
]

cursor.executemany("INSERT INTO students VALUES (?, ?, ?)", rows)
connection.commit()


cursor.execute(
    "SELECT city, AVG(grade) FROM students GROUP BY city ORDER BY city"
)

by_city = {}
for row in cursor.fetchall():
    by_city[row[0]] = round(row[1])

best_city = ""
best_average = 0
for city in by_city:
    if by_city[city] > best_average:
        best_average = by_city[city]
        best_city = city


print(by_city)
print(best_city)
