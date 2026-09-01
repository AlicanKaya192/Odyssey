# Veritabanı Tuzakları

Veritabanı hataları iki gruba ayrılıyor: hemen hata verenler ve sessizce veri
kaybettirenler. İkinci grup daha tehlikeli.

## 1. `commit` unutmak

```python
cursor.execute("INSERT INTO students VALUES (?, ?)", ("Ada", 90))
connection.close()
```

Program hatasız çalışıyor. Ama dosyayı sonra açtığında Ada orada değil.

Veritabanı değişiklikleri bir **işlem** içinde tutuyor ve `commit` çağrılana
kadar kalıcı yapmıyor. `close` çağrıldığında kaydedilmemiş işlem geri
alınıyor.

`SELECT` için gerekmiyor; yalnızca `INSERT`, `UPDATE`, `DELETE` ve
`CREATE` için.

Unutmamanın yolu `with` kullanmak:

```python
with sqlite3.connect("school.db") as connection:
    cursor = connection.cursor()
    cursor.execute("INSERT INTO students VALUES (?, ?)", ("Ada", 90))
```

Blok hatasız biterse `commit` kendiliğinden çağrılıyor, hata çıkarsa geri
alınıyor.

**Ama dikkat:** dosyalardaki `with`'ten farklı olarak bu **bağlantıyı
kapatmıyor.** Kapatmayı ayrıca yapman gerekiyor.

## 2. Değeri komuta yapıştırmak

```python
name = "O'Brien"
cursor.execute("INSERT INTO students VALUES ('" + name + "', 90)")
```

```
sqlite3.OperationalError: near "Brien": syntax error
```

Ortadaki tırnak komutu ikiye bölüyor. Bu, iyi niyetli bir kullanıcının
adıyla oluşan hâli.

Kötü niyetli bir metin ise komutun anlamını değiştirebiliyor — buna **SQL
enjeksiyonu** deniyor ve yazılım güvenliğinin en eski açıklarından biri.

Çözüm her zaman aynı:

```python
cursor.execute("INSERT INTO students VALUES (?, ?)", (name, 90))
```

Yer tutucu kullandığında kütüphane değeri **veri** olarak yerleştiriyor,
komutun parçası olarak değil. İkisi arasındaki fark tam olarak bu.

## 3. Tek elemanlı demette virgül unutmak

```python
cursor.execute("SELECT name FROM students WHERE city = ?", ("London"))
```

```
ValueError: parameters are of unsupported type
```

`("London")` bir demet değil — parantez içinde bir metin. Python'da demet
virgülle oluşuyor:

```python
cursor.execute("SELECT name FROM students WHERE city = ?", ("London",))
```

Sondaki virgül tuhaf görünüyor ama gerekli. Liste de kullanılabilir:

```python
cursor.execute("SELECT name FROM students WHERE city = ?", ["London"])
```

## 4. `WHERE` unutmak

```python
cursor.execute("UPDATE students SET grade = 0")
cursor.execute("DELETE FROM students")
```

İkisi de hatasız çalışıyor. Birincisi bütün notları sıfırlıyor, ikincisi
tabloyu boşaltıyor. Geri alma yok.

Alışkanlık edinmeye değer: silme veya güncelleme yazarken önce `WHERE`
kısmını yaz, sonra başını.

Bir de kontrol yöntemi var — önce `SELECT` ile bak:

```python
cursor.execute("SELECT COUNT(*) FROM students WHERE grade < 50")
print(cursor.fetchone()[0])       # kac satir etkilenecek?
```

## 5. `fetchall` sonrası tekrar okumak

```python
cursor.execute("SELECT name FROM students")
first = cursor.fetchall()
second = cursor.fetchall()

print(len(first), len(second))
```

```
3 0
```

Sonuç kümesi bir kez okunuyor, tıpkı dosyadaki okuma imleci gibi. İkinci
`fetchall` boş liste veriyor.

Çözüm: bir kez oku, değişkende tut.

## 6. `fetchone` sonucunu kontrol etmemek

```python
cursor.execute("SELECT name FROM students WHERE grade > 200")
row = cursor.fetchone()

print(row[0])
```

```
TypeError: 'NoneType' object is not subscriptable
```

Sonuç yoksa `fetchone` `None` döndürüyor. Kontrol etmen gerekiyor:

```python
row = cursor.fetchone()
if row is None:
    print("not found")
else:
    print(row[0])
```

Tip belirtimi diliyle: `fetchone` dönüşü `tuple | None`.

## 7. Satırın demet olduğunu unutmak

```python
cursor.execute("SELECT COUNT(*) FROM students")
print(cursor.fetchone())
```

```
(3,)
```

Beklediğin `3`, gelen `(3,)`. Tek sütun istesen bile satır demet olarak
geliyor. Değeri almak için indeks gerekiyor:

```python
print(cursor.fetchone()[0])
```

```
3
```

## 8. SQLite tip konusunda esnek

```python
cursor.execute("CREATE TABLE students (name TEXT, grade INTEGER)")
cursor.execute("INSERT INTO students VALUES (?, ?)", ("Ada", "not a number"))
connection.commit()
```

Hata yok. SQLite sütun tipini bir **öneri** sayıyor ve uymayan değeri de
kabul ediyor. Diğer veritabanlarının çoğu bunu reddediyor.

Bunun anlamı: veriyi doğrulama işi **sana** kalıyor. `int()` çevirisini
`try` / `except` ile korumak burada işe yarıyor.

## 9. Bağlantıyı kapatmamak

```python
connection = sqlite3.connect("school.db")
# ... is bitti ama close cagrilmadi
```

Küçük betiklerde çoğunlukla sorun çıkmıyor; program bitince işletim sistemi
temizliyor. Ama dosya açık kaldığı sürece kilitli sayılıyor ve başka bir
işlem yazmaya çalışırsa `database is locked` hatası alıyor.

Uzun çalışan bir programda bağlantı sızıntısı gerçek bir sorun.

## Özet

| Tuzak | Sonucu |
|---|---|
| `commit` unutmak | Değişiklikler kaybolur |
| Değeri metne gömmek | Hata veya SQL enjeksiyonu |
| Demette virgül unutmak | `unsupported type` |
| `WHERE` unutmak | Bütün tablo etkilenir |
| İki kez `fetchall` | İkincisi boş gelir |
| `fetchone` kontrolsüz | `NoneType` hatası |
| Demeti unutmak | `(3,)` beklerken `3` |
| Tipe güvenmek | Yanlış tip sessizce girer |
| Bağlantıyı kapatmamak | `database is locked` |
