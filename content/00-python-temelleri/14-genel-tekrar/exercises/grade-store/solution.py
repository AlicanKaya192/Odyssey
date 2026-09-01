import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

cursor.execute("CREATE TABLE grades (name TEXT, grade INTEGER)")


def save(name: str, raw: str) -> bool:
    try:
        grade = int(raw)
    except ValueError:
        return False
    cursor.execute("INSERT INTO grades VALUES (?, ?)", (name, grade))
    connection.commit()
    return True


def find(name: str) -> int | None:
    cursor.execute("SELECT grade FROM grades WHERE name = ?", (name,))
    row = cursor.fetchone()
    if row is None:
        return None
    return row[0]


def average() -> int:
    cursor.execute("SELECT AVG(grade) FROM grades")
    row = cursor.fetchone()
    if row[0] is None:
        return 0
    return round(row[0])


print(save("Ada", "90"))
print(save("Brian", "oops"))
print(save("Grace", "76"))

print(find("Ada"))
print(find("Nobody"))
print(average())
