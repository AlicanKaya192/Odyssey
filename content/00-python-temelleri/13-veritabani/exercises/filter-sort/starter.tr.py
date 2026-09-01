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


# passing: notu 50 ve ustu olanlar, nottan buyukten kucuge sirali.
# Yalnizca name ve grade sutunlari.


# londoners: sehri London olanlarin adlari, liste olarak.


# Once passing, sonra londoners yazdir.
