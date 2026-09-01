# SQL Sözlüğü

Bu bölümde kullanacağın SQL komutlarının listesi. Takıldığında buraya bak.

SQL, Python değil — ayrı bir dil. Veritabanına ne istediğini SQL ile
söylüyorsun, Python yalnızca o metni taşıyor.

## Tablo kurmak

```sql
CREATE TABLE students (
    name TEXT,
    grade INTEGER,
    city TEXT
)
```

Tablo varsa hata vermemesi için:

```sql
CREATE TABLE IF NOT EXISTS students (name TEXT, grade INTEGER)
```

### Sütun kısıtları

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    grade INTEGER DEFAULT 0
)
```

| Kısıt | Ne yapar |
|---|---|
| `PRIMARY KEY` | Satırı benzersiz tanımlar |
| `NOT NULL` | Boş bırakılamaz |
| `DEFAULT x` | Değer verilmezse `x` kullanılır |
| `UNIQUE` | Aynı değer iki kez giremez |

`INTEGER PRIMARY KEY` yazdığında SQLite o sütunu **kendisi dolduruyor** —
her yeni satıra bir sonraki sayıyı veriyor. Bu yüzden `INSERT` sırasında o
sütunu atlayabiliyorsun.

## Veri eklemek

Bütün sütunlara sırayla:

```sql
INSERT INTO students VALUES (?, ?, ?)
```

Belirli sütunlara:

```sql
INSERT INTO students (name, grade) VALUES (?, ?)
```

İkinci yazım daha güvenli: tabloya sonradan sütun eklenirse komut bozulmuyor.

## Okumak

```sql
SELECT name, grade FROM students
SELECT * FROM students
```

`*` bütün sütunlar demek. Gerçek kodda tek tek yazmak tercih ediliyor —
`*` kullanınca sütun sırası değişince kodun sessizce bozuluyor.

### Süzmek

```sql
SELECT name FROM students WHERE grade >= 50
```

| Operatör | Anlamı |
|---|---|
| `=` | Eşit (Python'daki `==` değil, tek eşittir) |
| `!=` veya `<>` | Eşit değil |
| `>` `<` `>=` `<=` | Karşılaştırma |
| `AND` `OR` `NOT` | Mantık (Python'daki gibi) |
| `IN (a, b)` | Şunlardan biri |
| `BETWEEN a AND b` | Aralıkta |
| `LIKE 'A%'` | Metin deseni — `%` herhangi bir şey |
| `IS NULL` | Boş mu |

Dikkat: SQL'de eşitlik **tek eşittir**. Python alışkanlığıyla `==` yazarsan
SQLite bunu kabul ediyor ama başka veritabanları etmiyor.

Boşluk kontrolü `= NULL` ile yapılmıyor, `IS NULL` ile yapılıyor.

### Sıralamak ve sınırlamak

```sql
SELECT name, grade FROM students
ORDER BY grade DESC
LIMIT 3
```

`LIMIT` ilk kaç satırı istediğini söylüyor. Büyük tablolarda hayat kurtarıyor.

## Hesap yaptırmak

```sql
SELECT COUNT(*) FROM students
SELECT AVG(grade) FROM students
SELECT MAX(grade), MIN(grade) FROM students
```

### Gruplayarak

```sql
SELECT city, COUNT(*), AVG(grade)
FROM students
GROUP BY city
```

Her şehir için ayrı bir satır dönüyor. Gruplanmış sonucu süzmek istersen
`WHERE` değil `HAVING` kullanılıyor:

```sql
SELECT city, AVG(grade)
FROM students
GROUP BY city
HAVING AVG(grade) > 70
```

Fark şu: `WHERE` gruplamadan **önce** satırları süzüyor, `HAVING` gruplamadan
**sonra** grupları süzüyor.

## Değiştirmek

```sql
UPDATE students SET grade = ? WHERE name = ?
DELETE FROM students WHERE grade < ?
```

**`WHERE` olmadan ikisi de bütün tabloyu etkiliyor.** Geri alma yok.

Bir alışkanlık edinmek işe yarıyor: silme komutunu önce `SELECT` olarak yaz,
kaç satır geldiğini gör, sonra `DELETE` yap.

```sql
SELECT * FROM students WHERE grade < 50      -- once bak
DELETE FROM students WHERE grade < 50        -- sonra sil
```

## Python tarafı

| Python | Ne yapar |
|---|---|
| `sqlite3.connect(yol)` | Bağlanır, dosya yoksa oluşturur |
| `connection.cursor()` | Komut çalıştırıcı verir |
| `cursor.execute(sql, degerler)` | Tek komut çalıştırır |
| `cursor.executemany(sql, satirlar)` | Aynı komutu çok satırla çalıştırır |
| `cursor.fetchall()` | Bütün sonuç satırlarını liste olarak verir |
| `cursor.fetchone()` | Tek satır verir, yoksa `None` |
| `cursor.lastrowid` | Son eklenen satırın `id` değeri |
| `cursor.rowcount` | Son komutun etkilediği satır sayısı |
| `connection.commit()` | Değişiklikleri kalıcı yapar |
| `connection.close()` | Bağlantıyı kapatır |

## Satırları sözlük olarak almak

Varsayılan olarak satırlar demet geliyor ve sütuna sırayla erişiyorsun:

```python
row = cursor.fetchone()
print(row[0])
```

Sıra kolayca karışıyor. Adla erişmek daha güvenli:

```python
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("SELECT name, grade FROM students")
row = cursor.fetchone()

print(row["name"], row["grade"])
```

Bu satırı bağlantıyı kurduktan hemen sonra yazıyorsun; `cursor` ondan sonra
alınmalı.

## Sonraki adım

Buradaki komutlar SQL'in temel katmanı. SQL patikasında bunların üstüne
`JOIN` geliyor — iki tabloyu birleştirmek. O da bu bilgi olmadan
öğrenilmiyor.
