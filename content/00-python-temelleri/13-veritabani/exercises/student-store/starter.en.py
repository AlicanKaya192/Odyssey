import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

cursor.execute("CREATE TABLE students (name TEXT, grade INTEGER)")


# add_student(name, grade): inserts a row, commits and returns
# the total number of rows in the table.


# update_grade(name, grade): updates the grade, commits and returns
# the number of affected rows.


# find_grade(name): returns the grade, or None if the name is not there.


# Call these in order and print each result:
# add_student("Ada", 90), add_student("Brian", 40),
# update_grade("Ada", 95), find_grade("Ada"), find_grade("Nobody")
