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


# by_city: anahtar sehir, deger o sehrin ortalamasi (tam sayiya yuvarlanmis).
# AVG ve GROUP BY kullan, sehirleri alfabetik getir.


# best_city: ortalamasi en yuksek sehrin adi.


# Once by_city, sonra best_city yazdir.
