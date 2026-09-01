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


# by_city: the city as the key, its average as the value (rounded to a whole
# number). Use AVG and GROUP BY, and bring the cities back alphabetically.


# best_city: the name of the city with the highest average.


# Print by_city first, then best_city.
