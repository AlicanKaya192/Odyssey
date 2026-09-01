import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

cursor.execute("CREATE TABLE grades (name TEXT, grade INTEGER)")


# save(name: str, raw: str) -> bool
# Insert and return True if raw converts to a number, otherwise return False.


# find(name: str) -> int | None


# average() -> int
# The average of the grades, rounded to a whole number. 0 if the table is empty.


# Save ("Ada", "90"), ("Brian", "oops") and ("Grace", "76") in order
# and print each result.
# Then print find("Ada"), find("Nobody") and average().
