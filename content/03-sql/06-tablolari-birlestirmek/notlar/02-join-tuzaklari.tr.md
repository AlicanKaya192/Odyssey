`JOIN` yazarken karşılaşacağın sorunlar. İlk ikisi hata veriyor; kalan
dördü **sessiz** ve sayıları yanlış çıkarıyor.

## Ambiguous column name 'X'

İki tabloda da aynı adlı bir sütun var ve hangisini istediğini
söylemedin.

```sql
SELECT name FROM products p JOIN categories c ON p.category_code = c.code;
-- Ambiguous column name 'name'
```

Bu şemada `name` sütunu **beş** tabloda birden var: `categories`,
`suppliers`, `products`, `customers`, `employees`.

Çözüm takma ad: `p.name`, `c.name`. Birden çok tabloyla çalışırken **her
sütunun önüne takma ad yazmak** iyi bir alışkanlık — sonradan bir `JOIN`
eklendiğinde sorgu bozulmuyor.

## The multi-part identifier could not be bound

Var olmayan bir takma adı kullandın:

```sql
FROM products p JOIN categories c ON prd.category_code = c.code
```

`prd` diye bir takma ad tanımlanmamış. Genelde takma adı değiştirip bir
yeri güncellemeyi unutmaktan çıkıyor.

---

## Sessiz hatalar

### 1. LEFT JOIN'i öldüren WHERE

En sık yapılan hata.

```sql
FROM products p
LEFT JOIN suppliers s ON p.supplier_code = s.code
WHERE s.country = 'Turkey'      -- 9 satir
```

Sağ tarafı boş gelen satırlarda `s.country` `NULL` oluyor ve `NULL =
'Turkey'` "bilinmiyor" olduğu için `WHERE` o satırları eliyor. `LEFT JOIN`
sessizce `INNER JOIN`'e dönüşüyor.

Koşul `ON` içine yazılınca sol taraf korunuyor:

```sql
LEFT JOIN suppliers s
  ON p.supplier_code = s.code
 AND s.country = 'Turkey'       -- 12 satir
```

**İstisna:** eşleşmeyenleri bulmak için `WHERE sag.sutun IS NULL` bilerek
yazılıyor.

### 2. Satır çoğalması

`orders` on satır, `order_items` yirmi satır. Birleştirince sonuç **yirmi**
satır oluyor: her siparişin bilgisi kalem sayısı kadar tekrar ediyor.

Somut sonuçları:

- `COUNT(*)` artık sipariş sayısını vermiyor → `COUNT(DISTINCT o.id)`
- `SUM(o.bir_sutun)` aynı değeri birden çok kez topluyor

İkincisi en tehlikelisi: sipariş başına bir kez sayılması gereken bir şey
kalem sayısı kadar sayılıyor ve toplam şişiyor. Hata yok, sadece yanlış
rakam.

### 3. LEFT JOIN'den sonra COUNT(*)

```sql
SELECT c.name, COUNT(*) FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id GROUP BY c.name;
```

Hiç siparişi olmayan müşteri için sonuç **1** çıkıyor, 0 değil. Çünkü
`LEFT JOIN` o müşteri için boş sütunlu bir satır üretiyor ve `COUNT(*)`
satırları sayıyor.

Doğrusu sağ tablonun bir sütununu saymak: `COUNT(o.id)` orada **0**
veriyor.

### 4. ON koşulu unutulan JOIN

```sql
FROM products p, categories c        -- eski yazim, ON yok
```

Bu, her ürünü her kategoriyle eşleştiriyor: 12 × 4 = **48** satır. Buna
kartezyen çarpım deniyor.

Modern yazımda `JOIN ... ON` kullanılıyor ve `ON` unutulursa sunucu hata
veriyor. Eski virgüllü yazım ise sessizce kartezyen üretiyor — bu yüzden
kullanılmıyor.

Bilerek yapmak istiyorsan adı var: `CROSS JOIN`.

---

## Kontrol alışkanlığı

`JOIN` yazdığında üç şeye bak:

1. **Satır sayısı beklediğin gibi mi?** Sol tablodan az geldiyse
   `INNER JOIN` satır düşürmüştür; çoksa çoğalma vardır.
2. **Bir satırı elle takip edebiliyor musun?** Bir sipariş numarası seçip
   sonucu gözle doğrulamak, on beş dakikalık aramayı önlüyor.
3. **`LEFT JOIN` yazdıysan, sağ tabloya koyduğun koşul nerede?** `WHERE`
   içindeyse muhtemelen `ON` içinde olmalıydı.
