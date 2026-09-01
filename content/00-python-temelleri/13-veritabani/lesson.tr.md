# Veritabanı İşlemleri

Önceki bölümde veriyi dosyaya yazdın. Bu, yüz satır için gayet iyi. Ama şunu
sormaya başladığında yetmiyor:

- "Notu 80'in üstünde olan öğrencileri getir."
- "Şehirlere göre ortalama notu hesapla."
- "Bu ismi güncelle, ama yalnızca bu satırda."

Dosyayla bunların hepsi elle döngü yazmak demek. **Veritabanı** bu soruları
kendisi cevaplıyor.

Bu bölümde `sqlite3` kullanacaksın. Python'un içinde geliyor — kurulum yok,
sunucu yok, hesap yok. Veritabanının tamamı tek bir dosya.

## Bağlanmak

```python
import sqlite3

connection = sqlite3.connect("school.db")
cursor = connection.cursor()

# ... isini yaparsin ...

connection.commit()
connection.close()
```

Dört adım var ve sırası önemli:

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>connect</b><br>dosyayı aç</span>
    <span class="arrow">→</span>
    <span class="node"><b>cursor</b><br>komut çalıştırıcı</span>
    <span class="arrow">→</span>
    <span class="node"><b>execute</b><br>SQL komutu</span>
    <span class="arrow">→</span>
    <span class="node ok"><b>commit</b><br>diske yaz</span>
  </div>
  <figcaption>commit çağrılmazsa yaptığın değişiklikler diske hiç geçmiyor — program kapandığında hepsi kayboluyor.</figcaption>
</figure>

Dosya yoksa `connect` onu oluşturuyor. Bellekte, geçici bir veritabanı da
kurulabiliyor:

```python
connection = sqlite3.connect(":memory:")
```

Bu, denemeler için ideal: program bitince kayboluyor, diskte iz kalmıyor.

## Tablo oluşturmak

Veritabanında veri **tablolarda** duruyor. Tablo, sütunları ve her sütunun
tipi belli olan bir yapı:

```python
cursor.execute("""
    CREATE TABLE students (
        name TEXT,
        grade INTEGER,
        city TEXT
    )
""")
```

Kullanacağın tipler:

| SQL tipi | Python karşılığı |
|---|---|
| `TEXT` | `str` |
| `INTEGER` | `int` |
| `REAL` | `float` |
| `NULL` | `None` |

Tablo zaten varsa komut hata veriyor. Bunu önlemek için:

```python
cursor.execute("CREATE TABLE IF NOT EXISTS students (name TEXT, grade INTEGER)")
```

## Veri eklemek

```python
cursor.execute("INSERT INTO students VALUES (?, ?)", ("Ada", 90))
```

Soru işaretleri **yer tutucu**. Değerleri ikinci argümanda demet olarak
veriyorsun.

Birden fazla satırı tek seferde eklemek için `executemany`:

```python
rows = [("Ada", 90), ("Brian", 40), ("Grace", 75)]
cursor.executemany("INSERT INTO students VALUES (?, ?)", rows)
```

## Soru işareti neden önemli?

Değeri komutun içine doğrudan yazmak mümkün ama **yapılmıyor**:

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h5>METNE GÖMMEK — TEHLİKELİ</h5>
<pre><code>cursor.execute(
    "INSERT INTO students VALUES ('" + name + "', 90)"
)</code></pre>
    </div>
    <div class="ok">
      <h5>YER TUTUCU — DOĞRU</h5>
<pre><code>cursor.execute(
    "INSERT INTO students VALUES (?, ?)",
    (name, 90)
)</code></pre>
    </div>
  </div>
  <figcaption>Soldaki yazımda <code>name</code> içindeki bir tırnak işareti komutu bozuyor; kasıtlı yazılmış bir metin ise komutun anlamını tamamen değiştirebiliyor. Buna SQL enjeksiyonu deniyor.</figcaption>
</figure>

Somut örnek: `name` değeri `O'Brien` olsun. Soldaki yazımda ortadaki tırnak
komutu ikiye bölüyor ve `sqlite3.OperationalError` alıyorsun. Sağdaki yazımda
hiçbir sorun yok — kütüphane değeri güvenle yerleştiriyor.

**Kural: değerler hiçbir zaman SQL metnine yapıştırılmaz, her zaman `?` ile
verilir.**

## Veri okumak

```python
cursor.execute("SELECT name, grade FROM students")
rows = cursor.fetchall()

print(rows)
```

```
[('Ada', 90), ('Brian', 40), ('Grace', 75)]
```

Her satır bir **demet** olarak geliyor. Tek satır istiyorsan:

```python
cursor.execute("SELECT name FROM students WHERE grade > 80")
row = cursor.fetchone()

print(row)
```

```
('Ada',)
```

Sonuç yoksa `fetchone` `None` döndürüyor — kontrol etmen gerekiyor.

Dikkat: `fetchall` bir kez çalışıyor. İkinci kez çağırırsan boş liste
geliyor, tıpkı bir dosyayı iki kez okumak gibi.

## Süzmek ve sıralamak

```python
cursor.execute("""
    SELECT name, grade FROM students
    WHERE grade >= 50
    ORDER BY grade DESC
""")

print(cursor.fetchall())
```

```
[('Ada', 90), ('Grace', 75)]
```

- `WHERE` koşul koyuyor — Python'daki `if` gibi.
- `ORDER BY` sıralıyor; `DESC` büyükten küçüğe, `ASC` (varsayılan) küçükten
  büyüğe.

Koşulda da yer tutucu kullanılıyor:

```python
cursor.execute("SELECT name FROM students WHERE city = ?", ("London",))
```

Tek elemanlı demette virgül şart: `("London",)`. Virgülsüz yazarsan bu bir
demet değil, sadece parantez içinde bir metin olur ve hata alırsın.

## Hesap yaptırmak

Veritabanının asıl gücü burada. Python'da döngü yazmadan:

```python
cursor.execute("SELECT COUNT(*) FROM students")
print(cursor.fetchone()[0])

cursor.execute("SELECT AVG(grade) FROM students")
print(cursor.fetchone()[0])

cursor.execute("""
    SELECT city, AVG(grade) FROM students
    GROUP BY city
""")
print(cursor.fetchall())
```

`GROUP BY` şehirlere göre grupluyor ve her grup için ortalamayı ayrı
hesaplıyor. Bunu Python'da yazmak on satır sürerdi.

| Fonksiyon | Ne yapar |
|---|---|
| `COUNT(*)` | Satır sayısı |
| `SUM(sutun)` | Toplam |
| `AVG(sutun)` | Ortalama |
| `MIN` / `MAX` | En küçük / en büyük |

## Güncellemek ve silmek

```python
cursor.execute("UPDATE students SET grade = ? WHERE name = ?", (95, "Ada"))
cursor.execute("DELETE FROM students WHERE grade < ?", (50,))
connection.commit()
```

**`WHERE` yazmayı unutma.** `WHERE` olmadan `UPDATE` bütün satırları
değiştiriyor, `DELETE` bütün tabloyu boşaltıyor. Geri alma yok.

## `commit` unutmak

En sık yapılan hata bu:

```python
cursor.execute("INSERT INTO students VALUES (?, ?)", ("Ada", 90))
connection.close()
```

Program çalışıyor, hata yok. Ama sonra dosyayı açtığında Ada orada değil.

Sebebi: veritabanı değişiklikleri bir **işlem** (transaction) içinde tutuyor
ve `commit` çağrılana kadar kalıcı hâle getirmiyor. `close` çağrıldığında
kaydedilmemiş işlem geri alınıyor.

Okuma komutları (`SELECT`) için `commit` gerekmiyor; yalnızca değişiklik
yapan komutlar için.

## Özet

- `sqlite3` Python'un içinde geliyor; sunucu, kurulum ve hesap gerektirmiyor.
- Sıra: `connect` → `cursor` → `execute` → `commit` → `close`.
- Veri **tablolarda** durur; tablo `CREATE TABLE` ile kurulur.
- Değerler SQL metnine **yapıştırılmaz**, `?` yer tutucusuyla verilir.
- `SELECT` okur, `fetchall` bütün satırları, `fetchone` tek satırı verir.
- `WHERE` süzer, `ORDER BY` sıralar, `GROUP BY` gruplar.
- `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` hesabı veritabanına yaptırır.
- `UPDATE` ve `DELETE` komutlarında `WHERE` unutmak bütün tabloyu etkiler.
- `commit` çağrılmazsa değişiklikler kaybolur.
