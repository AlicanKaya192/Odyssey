import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

cursor.execute("CREATE TABLE students (name TEXT, grade INTEGER)")


def add_student(name, grade):
    cursor.execute("INSERT INTO students VALUES (?, ?)", (name, grade))
    connection.commit()
    cursor.execute("SELECT COUNT(*) FROM students")
    return cursor.fetchone()[0]


def update_grade(name, grade):
    cursor.execute("UPDATE students SET grade = ? WHERE name = ?", (grade, name))
    connection.commit()
    return cursor.rowcount


def find_grade(name):
    cursor.execute("SELECT grade FROM students WHERE name = ?", (name,))
    row = cursor.fetchone()
    if row is None:
        return None
    return row[0]


print(add_student("Ada", 90))
print(add_student("Brian", 40))
print(update_grade("Ada", 95))
print(find_grade("Ada"))
print(find_grade("Nobody"))
