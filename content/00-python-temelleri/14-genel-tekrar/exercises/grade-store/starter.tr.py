import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

cursor.execute("CREATE TABLE grades (name TEXT, grade INTEGER)")


# save(name: str, raw: str) -> bool
# raw sayiya cevrilebiliyorsa ekle ve True dondur, yoksa False dondur.


# find(name: str) -> int | None


# average() -> int
# Notlarin ortalamasi, tam sayiya yuvarlanmis. Tablo bossa 0.


# Sirayla ("Ada", "90"), ("Brian", "oops"), ("Grace", "76") kaydet
# ve her sonucu yazdir.
# Sonra find("Ada"), find("Nobody") ve average() yazdir.
