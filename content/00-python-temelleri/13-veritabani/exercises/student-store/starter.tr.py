import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

cursor.execute("CREATE TABLE students (name TEXT, grade INTEGER)")


# add_student(name, grade): satir ekler, commit eder,
# tablodaki toplam satir sayisini dondurur.


# update_grade(name, grade): notu gunceller, commit eder,
# etkilenen satir sayisini dondurur.


# find_grade(name): notu dondurur, isim yoksa None dondurur.


# Sirayla cagir ve her sonucu yazdir:
# add_student("Ada", 90), add_student("Brian", 40),
# update_grade("Ada", 95), find_grade("Ada"), find_grade("Nobody")
