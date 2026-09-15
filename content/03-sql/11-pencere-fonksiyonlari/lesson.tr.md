# Pencere Fonksiyonları

`GROUP BY` satırları topluyor: on iki ürün dört kategoriye iniyor ve
ürünlerin kendisi kayboluyor. Çoğu zaman ikisi birden gerekiyor — **hem
satırın kendisi hem de ait olduğu grubun bilgisi.** "Bu ürün kendi
kategorisinde kaçıncı?", "Bu siparişle ciro nereye geldi?", "Müşterinin
bir önceki siparişi ne zamandı?"

Pencere fonksiyonları bunu yapıyor: satırları **toplamadan**, her satırın
yanına bir hesap ekliyor. İleri Seviye buradan başlıyor; şema Orta
Seviyenin sekiz tablolu sipariş veritabanı ve aşağıdaki her sonuç onun
üstünde ölçüldü.

## GROUP BY ile OVER

<figure class="fig">
  <div class="versus">
    <div>
      <h4>GROUP BY</h4>
      <pre><code>SELECT category_code, MAX(price)
FROM products
GROUP BY category_code;</code></pre>
      <p>4 satır: her kategori bir satır, ürünler kayboldu.</p>
    </div>
    <div>
      <h4>OVER</h4>
      <pre><code>SELECT name, category_code,
  MAX(price) OVER (
    PARTITION BY category_code)
FROM products;</code></pre>
      <p>12 satır: her ürün yerinde, yanında kendi kategorisinin en yüksek fiyatı.</p>
    </div>
  </div>
</figure>

Ölçüldü: `GROUP BY` ile 4, `PARTITION BY` ile 12 satır.

`OVER` gördüğün yerde bir pencere fonksiyonu var. Bildiğin toplama
işlevleri (`SUM`, `COUNT`, `AVG`, `MAX`) `OVER` ile yazılınca pencere
fonksiyonu oluyor; bir de yalnızca pencereyle çalışan yeni işlevler var:
`ROW_NUMBER`, `RANK`, `LAG`...

## OVER'ın içi

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">PARTITION BY</span><span class="anat-body">Satırları gruplara ayırıyor; hesap her grupta baştan başlıyor. Yazılmazsa bütün sonuç tek bir grup.</span></div>
    <div class="anat-row"><span class="anat-label">ORDER BY</span><span class="anat-body">Grubun içindeki sıra. Sıra numarası, birikimli toplam ve önceki satır bu sıraya göre hesaplanıyor.</span></div>
    <div class="anat-row"><span class="anat-label">ROWS ...</span><span class="anat-body">Çerçeve: hesaba grubun hangi satırlarının girdiği. Yazılmazsa bir varsayılan var — bölümün en sinsi tuzağı.</span></div>
  </div>
</figure>

Üçü de isteğe bağlı: `SUM(stock) OVER ()` bütün tablonun toplamını her
satıra yazıyor.

## Sıra numarası: ROW_NUMBER, RANK, DENSE_RANK

```sql
SELECT name, stock,
       ROW_NUMBER() OVER (ORDER BY stock DESC) AS rn,
       RANK()       OVER (ORDER BY stock DESC) AS rk,
       DENSE_RANK() OVER (ORDER BY stock DESC) AS drk
FROM products
ORDER BY stock DESC, name;
```

Ölçüldü (baştan ve sondan birer parça):

| name | stock | `ROW_NUMBER` | `RANK` | `DENSE_RANK` |
|---|---|---|---|---|
| Antivirus | 99 | 1 | 1 | 1 |
| Office Suite | 99 | 2 | 1 | 1 |
| Cable | 60 | 3 | **3** | **2** |
| Keyboard | 32 | 4 | 4 | 3 |
| … | | | | |
| Mouse | 0 | 11 | 11 | 10 |
| Projector | 0 | 12 | 11 | 10 |

Üçü yalnızca **eşitlikte** ayrışıyor:

- `ROW_NUMBER` herkese farklı numara veriyor, eşitleri de ayırıyor.
- `RANK` eşitlere aynı numarayı verip sonra **atlıyor**: 1, 1, 3.
- `DENSE_RANK` atlamıyor: 1, 1, 2.

**Eşitlerden hangisinin önce geldiği belli değil.** Aynı
`ROW_NUMBER() OVER (ORDER BY stock DESC)` iki ayrı sorguda çalıştırıldı:
birinde 1 numarayı Antivirus aldı, ötekinde Office Suite. Hata değil, ama
tekrarlanabilir de değil. Ayırt edici bir sütun bunu sabitliyor:
`ORDER BY stock DESC, name`.

`ROW_NUMBER() OVER ()` ise hata veriyor:
`The function 'ROW_NUMBER' must have an OVER clause with ORDER BY.`
Sıra numarası, neye göre verildiği söylenmeden verilemiyor.

## Her grubun en iyisi

"Her kategorinin en pahalı ürünü": `GROUP BY` ile `MAX(price)` fiyatı
buluyor ama ürünün **adını** getirmiyor. Pencereyle:

```sql
SELECT category_code, name, price
FROM (
    SELECT category_code, name, price,
           ROW_NUMBER() OVER (PARTITION BY category_code
                              ORDER BY price DESC) AS rn
    FROM products
) AS ranked
WHERE rn = 1;
```

| category_code | name | price |
|---|---|---|
| ACC | Microphone | 1320.00 |
| COM | Laptop | 24500.00 |
| DIS | Projector | 7400.00 |
| SOF | Office Suite | 2400.00 |

Neden iç içe? Çünkü iki kısa yol da hata veriyor (ölçüldü):

| Yazım | Sonuç |
|---|---|
| `WHERE ROW_NUMBER() OVER (...) = 1` | `Windowed functions can only appear in the SELECT or ORDER BY clauses.` |
| `SELECT ..., ROW_NUMBER() OVER (...) AS rn ... WHERE rn = 1` | `Invalid column name 'rn'.` |

`WHERE`, `SELECT`'ten **önce** çalışıyor; numara da takma ad da orada
henüz yok. Numaralı sorguyu `FROM (...)` içine alınca dıştaki `WHERE` onu
hazır bir sütun olarak görüyor. Bir sonraki bölümdeki `WITH` aynı işi
daha okunur yazacak.

## Birikimli toplam

```sql
SELECT o.id, o.order_date,
       SUM(i.quantity * i.unit_price) AS total,
       SUM(SUM(i.quantity * i.unit_price))
           OVER (ORDER BY o.order_date) AS running_total
FROM orders o
JOIN order_items i ON i.order_id = o.id
WHERE o.status <> 'cancelled'
GROUP BY o.id, o.order_date
ORDER BY o.order_date;
```

`SUM(SUM(...))` ilk bakışta garip: içteki `SUM` gruplamanın toplamı
(siparişin tutarı), dıştaki pencere — o tarihe kadar gelen tutarları
topluyor. Pencere gruplamadan **sonra** çalıştığı için ikisi birlikte
yazılabiliyor.

| id | order_date | total | running_total |
|---|---|---|---|
| 1001 | 2026-01-08 | 1815.00 | 1815.00 |
| 1002 | 2026-01-15 | 30900.00 | 32715.00 |
| 1003 | 2026-02-02 | 2340.00 | 35055.00 |
| … | | | |
| 1010 | 2026-04-17 | 5110.00 | 99165.00 |

## Çerçeve tuzağı

`OVER (ORDER BY ...)` yazıp çerçeve yazmayınca sunucu bir varsayılan
kullanıyor: "baştan **bu değere** kadar". Değer diyor, satır değil — aynı
değerdeki satırlar hep birlikte giriyor. Sıra sütununda eşitlik varsa
birikimli toplam sessizce bozuluyor. Ölçüldü, sipariş kalemleri
`order_id` sırasında:

```sql
SUM(quantity * unit_price) OVER (ORDER BY order_id)                      -- varsayilan
SUM(quantity * unit_price) OVER (ORDER BY order_id ROWS UNBOUNDED PRECEDING)
```

| order_id | product_id | line | varsayılan | `ROWS` ile |
|---|---|---|---|---|
| 1001 | 1 | 900.00 | **1815.00** | 900.00 |
| 1001 | 3 | 440.00 | **1815.00** | 1340.00 |
| 1001 | 9 | 475.00 | 1815.00 | 1815.00 |
| 1002 | 2 | 6400.00 | **32715.00** | 8215.00 |
| 1002 | 4 | 24500.00 | 32715.00 | 32715.00 |

Varsayılanda 1001'in üç kalemi de 1815 gösteriyor: üçü de "aynı değer"
sayıldı. `ROWS` satır satır sayıyor. Eşitler arasındaki sıra da önemliyse
ayırt edici bir sütun ekleniyor: `ORDER BY order_id, product_id`.

Çerçevenin yazımı:

| Çerçeve | Hesaba giren satırlar | Ne için |
|---|---|---|
| `ROWS UNBOUNDED PRECEDING` | baştan bu satıra kadar | birikimli toplam |
| `ROWS BETWEEN 1 PRECEDING AND CURRENT ROW` | bir önceki satır ve bu satır | hareketli ortalama |
| `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` | grubun tamamı | `LAST_VALUE` gibi |

`RANGE` ile sayı yazılamıyor: `RANGE BETWEEN 1 PRECEDING AND CURRENT ROW`
→ `RANGE is only supported with UNBOUNDED and CURRENT ROW window frame
delimiters.` (ölçüldü). Satır saymak için `ROWS`.

## Önceki ve sonraki satır: LAG, LEAD

Aylık ciro (iptal edilenler hariç) ve bir önceki aya göre değişim:

```sql
SELECT month, revenue,
       LAG(revenue)  OVER (ORDER BY month) AS prev_revenue,
       revenue - LAG(revenue) OVER (ORDER BY month) AS change,
       LEAD(revenue) OVER (ORDER BY month) AS next_revenue
FROM (
    SELECT DATEFROMPARTS(YEAR(o.order_date), MONTH(o.order_date), 1) AS month,
           SUM(i.quantity * i.unit_price) AS revenue
    FROM orders o
    JOIN order_items i ON i.order_id = o.id
    WHERE o.status <> 'cancelled'
    GROUP BY DATEFROMPARTS(YEAR(o.order_date), MONTH(o.order_date), 1)
) AS monthly
ORDER BY month;
```

| month | revenue | prev_revenue | change | next_revenue |
|---|---|---|---|---|
| 2026-01-01 | 32715.00 | NULL | NULL | 28680.00 |
| 2026-02-01 | 28680.00 | 32715.00 | −4035.00 | 7710.00 |
| 2026-03-01 | 7710.00 | 28680.00 | **−20970.00** | 30060.00 |
| 2026-04-01 | 30060.00 | 7710.00 | 22350.00 | NULL |

İlk ayın öncesi yok: `LAG` `NULL` veriyor, fark da `NULL`. Üçüncü
argüman bu durumdaki değeri değiştiriyor: `LAG(revenue, 1, 0)` Ocak'ta
`0.00` verdi. İkinci argüman kaç satır geri bakılacağı.

`PARTITION BY` ile her müşterinin kendi geçmişi:

```sql
SELECT customer_id, id, order_date,
       DATEDIFF(day,
                LAG(order_date) OVER (PARTITION BY customer_id
                                      ORDER BY order_date),
                order_date) AS gap_days
FROM orders
ORDER BY customer_id, order_date;
```

| customer_id | id | order_date | gap_days |
|---|---|---|---|
| 1 | 1001 | 2026-01-08 | NULL |
| 1 | 1003 | 2026-02-02 | 25 |
| 1 | 1006 | 2026-03-03 | 29 |
| 2 | 1002 | 2026-01-15 | NULL |
| 2 | 1008 | 2026-03-22 | 66 |

`PARTITION BY` olmasa bütün siparişler tek sıraya girer ve 1003'ün
"öncesi" 1002 olurdu — başka bir müşterinin siparişi.

## Toplamın payı

`OVER ()` — boş pencere — bütün sonucun toplamını her satıra yazıyor. Pay
hesabı bununla tek sorguda:

```sql
SELECT p.category_code,
       SUM(i.quantity * i.unit_price) AS revenue,
       CAST(100.0 * SUM(i.quantity * i.unit_price)
            / SUM(SUM(i.quantity * i.unit_price)) OVER ()
            AS DECIMAL(5,2)) AS share
FROM order_items i
JOIN products p ON p.id = i.product_id
JOIN orders o ON o.id = i.order_id
WHERE o.status <> 'cancelled'
GROUP BY p.category_code
ORDER BY revenue DESC;
```

| category_code | revenue | share |
|---|---|---|
| COM | 67900.00 | 68.47 |
| DIS | 12800.00 | 12.91 |
| ACC | 12165.00 | 12.27 |
| SOF | 6300.00 | 6.35 |

Hepsi `99165.00` üzerinden — birikimli toplamın son satırıyla aynı sayı.
`WHERE` unutulursa SOF `8700.00` oluyor: iptal edilen 1006 siparişindeki
Office Suite (2400) içeri giriyor.

## Birkaç araç daha

| İşlev | Ne veriyor | Ölçüldü |
|---|---|---|
| `COUNT(*) OVER (PARTITION BY customer_id)` | Müşterinin sipariş sayısı, her satırında | 1001 satırında 3 |
| `NTILE(4) OVER (ORDER BY price)` | Satırları 4 eşit gruba bölüyor | 12 ürün → 3'er |
| `NTILE(5) OVER (ORDER BY price)` | Eşit bölünmezse baştaki gruplar büyük | 3, 3, 2, 2, 2 |
| `FIRST_VALUE(name) OVER (ORDER BY price)` | Sıradaki ilk değer | ACC'de her satırda Cable |
| `AVG(stock) OVER ()` | Tam sayı sütunda **tam sayı** | ACC'de 19 (doğrusu 19,33) |

`LAST_VALUE` ise çerçeve tuzağına düşüyor: `LAST_VALUE(name) OVER (ORDER
BY price)` her satırda **satırın kendi adını** verdi, çünkü varsayılan
çerçeve o satırda bitiyor. Gerçekten sondakini almak için çerçeveyi
açmak gerekiyor: `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED
FOLLOWING` → her satırda Microphone.

## Pencere nerede yazılabiliyor

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">SELECT</span><span class="anat-body">Evet. Asıl yeri.</span></div>
    <div class="anat-row"><span class="anat-label">ORDER BY</span><span class="anat-body">Evet: <code>ORDER BY ROW_NUMBER() OVER (ORDER BY price DESC)</code> çalıştı.</span></div>
    <div class="anat-row"><span class="anat-label">WHERE, UPDATE ... SET</span><span class="anat-body">Hayır. İkisi de: <code>Windowed functions can only appear in the SELECT or ORDER BY clauses.</code></span></div>
  </div>
</figure>

Son bir not: `OVER` içindeki `ORDER BY` yalnızca **hesabın** sırası.
Sonucun satır sırası için sorgunun sonunda ayrıca `ORDER BY` yazılıyor.
Ölçümde sonuç bazen `OVER`'daki sırayla geldi, ama bu bir söz değil.

## Özet

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">OVER</span><span class="anat-body">Satırları toplamadan her satıra bir hesap ekliyor.</span></div>
    <div class="anat-row"><span class="anat-label">Sıra numarası</span><span class="anat-body"><code>ROW_NUMBER</code> / <code>RANK</code> / <code>DENSE_RANK</code>; eşitlikte ayırt edici bir sütun ekle.</span></div>
    <div class="anat-row"><span class="anat-label">Grubun ilki</span><span class="anat-body"><code>PARTITION BY</code>, iç sorgu, dışarıda <code>WHERE rn = 1</code>.</span></div>
    <div class="anat-row"><span class="anat-label">Birikimli toplam</span><span class="anat-body"><code>SUM(...) OVER (ORDER BY ... ROWS UNBOUNDED PRECEDING)</code>.</span></div>
    <div class="anat-row"><span class="anat-label">Önceki satır</span><span class="anat-body"><code>LAG</code>; sonraki <code>LEAD</code>; ilk satırda <code>NULL</code>.</span></div>
    <div class="anat-row"><span class="anat-label">Pay</span><span class="anat-body"><code>x / SUM(x) OVER ()</code>.</span></div>
  </div>
</figure>

Sıradaki bölüm `WITH`: bu bölümde defalarca yazdığın `FROM (...) AS
ranked` kalıbına bir ad vermek.
