Gruplamada karşılaşacağın hatalar ve ne demek istedikleri. İlk üçü sunucu
tarafından açıkça söyleniyor; son üçü **sessiz** ve daha tehlikeli.

## Column 'X' is invalid in the select list

Tam mesaj şöyle:

```
Column 'products.name' is invalid in the select list because it is not
contained in either an aggregate function or the GROUP BY clause.
```

Uzun ama tam olarak sorunu anlatıyor: `name` sütununu istedin ama hangi
satırın adı olacağını söylemedin.

`Accessory` grubunda altı ürün var. Sunucu bunlardan hangisinin adını
yazacağını bilemiyor ve tahmin etmiyor.

İki çıkış yolu var:

```sql
-- 1. sutunu gruplamaya ekle (daha kucuk gruplar olusur)
SELECT category, name, COUNT(*) FROM products GROUP BY category, name;

-- 2. hangisini istedigini soyle
SELECT category, MAX(name), COUNT(*) FROM products GROUP BY category;
```

İkisi farklı sonuç veriyor; hangisini istediğine karar etmen gerekiyor.

## An aggregate may not appear in the WHERE clause

```sql
WHERE COUNT(*) > 2      -- hata
```

`WHERE` gruplar oluşmadan **önce** çalışıyor. O anda sunucu tek tek
satırlara bakıyor ve ortada sayılacak bir grup yok.

Grupları süzen parça `HAVING`:

```sql
GROUP BY category HAVING COUNT(*) > 2
```

## Invalid column name (HAVING içinde)

```sql
SELECT category, COUNT(*) AS adet
FROM products
GROUP BY category
HAVING adet > 2         -- hata: Invalid column name 'adet'
```

Takma ad `SELECT` çalışırken oluşuyor; `HAVING` ondan **önce** çalışıyor.

Koşulu uzun hâliyle yazmak gerekiyor: `HAVING COUNT(*) > 2`.

Aynı takma ad `ORDER BY` içinde çalışıyor — o en sonda. Bu, patika boyunca
üçüncü kez karşına çıkan aynı kural.

---

## Sessiz hatalar

Bunlarda sorgu çalışıyor, sonuç geliyor, ama sayı yanlış.

### 1. WHERE ile HAVING'i karıştırmak

```sql
-- "stokta olan urunleri say" mi demek istedin...
WHERE stock > 0 GROUP BY category

-- ...yoksa "toplam stogu sifirdan buyuk olan kategoriler" mi?
GROUP BY category HAVING SUM(stock) > 0
```

İkisi tamamen farklı soru soruyor ve ikisi de çalışıyor. Birincisi
satırları eliyor, ikincisi grupları.

### 2. AVG'de tam sayı bölmesi

`AVG(stock)` **27** veriyor, gerçek ortalama 27,41. Sütun `INT` olduğu
için ondalık kısım atılıyor.

### 3. Boş sonuçta SUM'ın NULL vermesi

Hiç satır olmadığında `COUNT` sıfır ama `SUM` `NULL` veriyor. Rapor
hücresi boş çıkıyor ve "sıfır satış" ile "veri yok" birbirine karışıyor.

---

## Kontrol alışkanlığı

Gruplama sorgusu yazdığında üç soru sor:

1. **Kaç grup bekliyorum?** Gelen satır sayısı o mu? Fazlaysa gruplama
   listesinde olmaması gereken bir sütun var demektir.
2. **Grupların toplamı, gruplamadan önceki satır sayısını veriyor mu?**
   `COUNT(*)` değerlerini topla; `WHERE` yoksa toplam tablo satır sayısına
   eşit olmalı.
3. **Ortalama aldığım sütun tam sayı mı?** Öyleyse `CAST` gerekiyor.

İkinci soru özellikle işe yarıyor: tutmuyorsa ya bir `WHERE` unutulmuş ya
da beklenmedik bir `NULL` grubu var.
