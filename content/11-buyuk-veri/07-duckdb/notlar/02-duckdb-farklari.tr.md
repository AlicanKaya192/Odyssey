SQL patikasından gelen biri için DuckDB'de dikkat edilecekler. Hepsi bu
makinede denendi.

## 1. Bölme ondalıklı

```sql
SELECT 5 / 2, 5 // 2;      -- 2.5, 2
```

SQL Server'da iki tam sayının bölümü tam sayı (`5 / 2 = 2`); DuckDB'de
`/` ondalıklı sonuç veriyor. Tam sayı bölme için `//`.

## 2. `TOP` yok, `LIMIT` var

```sql
SELECT * FROM 'orders.parquet' ORDER BY unit_price DESC LIMIT 5;
```

## 3. Tarih işlevleri farklı

`FORMAT(tarih, 'yyyy-MM')` yerine `strftime(tarih, '%Y-%m')`; biçim
harfleri Python'unkiyle aynı.

## 4. Sütun adları büyük/küçük harfe duyarsız

`SELECT City FROM ...` sütun adı `city` olsa da çalışıyor.

## 5. CSV türleri tahmin ediliyor

DuckDB CSV'nin ilk satırlarına bakıp türleri seçiyor; tarihi `TIMESTAMP`
yapıyor. Başında sıfır olan posta kodunu (`01234`) metin olarak korudu.
pandas ise aynı sütunu sayıya çevirip `1234` yaptı. Tahmin yanlışsa türü
elle ver:

```sql
SELECT * FROM read_csv('zip.csv', types = {'zip': 'VARCHAR'});
```

## 6. `approx_` ile başlayanlar yaklaşık

`approx_count_distinct(city)` 8 şehir için 7 dedi; `SUMMARIZE`'daki
`approx_unique` da öyle. Kesin sayı için `count(DISTINCT city)`. Yaklaşık
sayım çok büyük veride çok az bellekle çalıştığı için var (Bölüm 9).

## 7. Geçici ve kalıcı

`duckdb.sql(...)` bellekte geçici bir veritabanı kullanıyor; `CREATE TABLE`
ile kurduğun tablo program kapanınca gidiyor. Saklamak için
`duckdb.connect("dosya.duckdb")`.

## 8. Metin birleştirme `||`

`'a' || 'b'` → `'ab'`. SQL Server'daki `+` ile metin birleştirme DuckDB'de
yok.
