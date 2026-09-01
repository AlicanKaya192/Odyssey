import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

cursor.execute("CREATE TABLE students (name TEXT, grade INTEGER)")

cursor.execute("INSERT INTO students VALUES (?, ?)", ("Ada", 90))
cursor.execute("INSERT INTO students VALUES (?, ?)", ("Brian", 40))

connection.commit()

cursor.execute("SELECT name, grade FROM students")
rows = cursor.fetchall()

print(rows)
print(len(rows))
