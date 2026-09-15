# WITH ve Özyineleme

Önceki bölümde aynı kalıbı defalarca yazdın: bir sorguyu `FROM (...)`
içine alıp dışarıda süzmek. Çalışıyor, ama okuması zor — sorgu içten
dışa okunuyor ve iç sorgunun adı en sonda geliyor.

`WITH` o iç sorguya **başta** bir ad veriyor. Sorgu yukarıdan aşağı
okunuyor: önce "şunu hazırla", sonra "hazırladığını kullan". Bir de
`FROM (...)` ile hiç yazılamayan bir şey yapabiliyor: **kendini
çağırmak.** Kaç kat olduğu bilinmeyen bir yönetim ağacı, ya da hiçbir
tabloda olmayan aylar bu sayede tek sorguda çıkıyor.

Aşağıdaki her sonuç Orta Seviyenin sekiz tablolu şemasında ölçüldü.

## WITH: sorguya ad vermek

<figure class="fig">
  <div class="versus">
    <div>
      <h4>FROM (...)</h4>
      <pre><code>SELECT category_code, name
FROM (
  SELECT category_code, name,
    ROW_NUMBER() OVER (
      PARTITION BY category_code
      ORDER BY price DESC) AS rn
  FROM products
) AS ranked
WHERE rn = 1;</code></pre>
      <p>İçten dışa: ad en sonda.</p>
    </div>
    <div>
      <h4>WITH</h4>
      <pre><code>WITH ranked AS (
  SELECT category_code, name,
    ROW_NUMBER() OVER (
      PARTITION BY category_code
      ORDER BY price DESC) AS rn
  FROM products
)
SELECT category_code, name
FROM ranked
WHERE rn = 1;</code></pre>
      <p>Yukarıdan aşağı: önce ad, sonra kullanım.</p>
    </div>
  </div>
</figure>

İkisi aynı dört ürünü getirdi (ölçüldü): Microphone, Laptop, Projector,
Office Suite. `WITH` ile tanımlanan şeye **CTE** deniyor (*common table
expression*, ortak tablo ifadesi): yalnızca o cümle boyunca yaşayan,
adlandırılmış bir sorgu.

## Bir adı iki kez kullanmak

`FROM (...)` ile yazılan iç sorgu bir kez kullanılabiliyor. CTE'nin adı
ise istediğin kadar. "Ortalamanın üstünde harcayan müşteriler":

```sql
WITH customer_totals AS (
    SELECT o.customer_id,
           SUM(i.quantity * i.unit_price) AS total
    FROM orders o
    JOIN order_items i ON i.order_id = o.id
    WHERE o.status <> 'cancelled'
    GROUP BY o.customer_id
)
SELECT c.name, ct.total
FROM customer_totals ct
JOIN customers c ON c.id = ct.customer_id
WHERE ct.total > (SELECT AVG(total) FROM customer_totals)
ORDER BY ct.total DESC;
```

| name | total |
|---|---|
| Helix Studio | 49690.00 |
| Bright Office | 34100.00 |

`customer_totals` iki yerde geçiyor: satırların kaynağı olarak ve
ortalamanın içinde. Beş müşterinin ortalaması `19833.00`; üstünde ikisi
kalıyor. `WITH` olmasa aynı gruplama iki kez yazılırdı.

## Zincir: birden fazla CTE

CTE'ler virgülle ayrılıyor ve her biri **kendinden öncekileri**
kullanabiliyor:

```sql
WITH order_totals AS (
    SELECT o.id, o.employee_id,
           SUM(i.quantity * i.unit_price) AS total
    FROM orders o
    JOIN order_items i ON i.order_id = o.id
    WHERE o.status <> 'cancelled'
    GROUP BY o.id, o.employee_id
),
employee_totals AS (
    SELECT employee_id, COUNT(*) AS orders, SUM(total) AS revenue
    FROM order_totals
    WHERE employee_id IS NOT NULL
    GROUP BY employee_id
)
SELECT e.name, et.orders, et.revenue
FROM employee_totals et
JOIN employees e ON e.id = et.employee_id
ORDER BY et.revenue DESC;
```

| name | orders | revenue |
|---|---|---|
| Deniz Kaya | 4 | 36700.00 |
| Ceren Aksoy | 3 | 35915.00 |

Her adım kendi başına okunabiliyor: önce sipariş tutarları, sonra
çalışan toplamları, en sonda adlar. İki toplama iç içe yazılamayacağı
için (`SUM(SUM(...))` ancak pencereyle olur) iki adım burada şart.

## Kurallar

Ölçüldü:

| Yazım | Sonuç |
|---|---|
| `SET NOCOUNT ON` ardından noktalı virgülsüz `WITH` | `Incorrect syntax near the keyword 'with'. ... the previous statement must be terminated with a semicolon.` |
| `SELECT ... FROM products` ardından noktalı virgülsüz `WITH` | `Incorrect syntax near 'x'. If this is intended to be a common table expression, you need to explicitly terminate the previous statement with a semi-colon.` |
| önceki cümle `;` ile bitince | çalışıyor |
| `;WITH ...` | çalışıyor |
| CTE'yi ikinci bir cümlede kullanmak | `Invalid object name 'x'.` |
| CTE içinde `ORDER BY` | `The ORDER BY clause is invalid in ... common table expressions, unless TOP, OFFSET or FOR XML is also specified.` |
| `WITH a AS (... FROM b), b AS (...)` | `Invalid object name 'b'.` |
| aynı adla iki CTE | `Duplicate common table expression name 'a' was specified.` |
| CTE içinde `WITH` | sözdizimi hatası |
| `WITH x (product, cost) AS (...)` | sütunlara ad veriyor; çalışıyor |

En sık karşılaşılanı ilk ikisi: `WITH` kelimesi T-SQL'de başka işlerde de
kullanıldığı için sunucu bir önceki cümlenin bittiğini bilmek istiyor.
Alışkanlık olarak önceki cümleyi `;` ile bitir. Bu uygulamada `WITH` ile
başlayan kod — başında yorum olsa bile — sorunsuz çalışıyor (ölçüldü).

## Özyineleme: kendini çağıran CTE

`employees` tablosunda her çalışanın `manager_id`'si var. "Herkes kaçıncı
kademede?" sorusu için kaç kat olduğunu bilmek gerekmiyor:

```sql
WITH chain AS (
    SELECT id, name, 0 AS level          -- baslangic
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, c.level + 1     -- kendini cagiran parca
    FROM employees e
    JOIN chain c ON e.manager_id = c.id
)
SELECT id, name, level FROM chain ORDER BY level, id;
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Başlangıç</span><span class="anat-body"><code>UNION ALL</code>'dan önceki sorgu. Bir kez çalışıyor: yöneticisi olmayan Ada.</span></div>
    <div class="anat-row"><span class="anat-label">UNION ALL</span><span class="anat-body">İki parçayı birleştiriyor. Özyinelemede <code>UNION</code> yazılamıyor.</span></div>
    <div class="anat-row"><span class="anat-label">Kendini çağıran parça</span><span class="anat-body"><code>FROM</code>'da CTE'nin kendi adı geçiyor. Her adımda bir önceki adımda <strong>yeni gelen</strong> satırlarla çalışıyor.</span></div>
    <div class="anat-row"><span class="anat-label">Durma</span><span class="anat-body">Parça hiç satır döndürmeyince özyineleme bitiyor.</span></div>
  </div>
</figure>

Adım adım:

<figure class="fig">
  <div class="flow">
    <span class="node acc">0 · Ada</span>
    <span class="arrow">→</span>
    <span class="node">1 · Bora, Emre</span>
    <span class="arrow">→</span>
    <span class="node">2 · Ceren, Deniz, Fulya</span>
    <span class="arrow">→</span>
    <span class="node no">3 · kimse yok, dur</span>
  </div>
</figure>

| id | name | level |
|---|---|---|
| 1 | Ada Kilic | 0 |
| 2 | Bora Yilmaz | 1 |
| 5 | Emre Sahin | 1 |
| 3 | Ceren Aksoy | 2 |
| 4 | Deniz Kaya | 2 |
| 6 | Fulya Demir | 2 |

`UNION` yazılınca hata: `Recursive common table expression 'chain' does
not contain a top-level UNION ALL operator.`

## Yolu yazmak: tip tuzağı

Kademe yerine zincirin kendisini yazmak — `Ada Kilic > Bora Yilmaz >
Ceren Aksoy` — aynı yapı, ama ilk denemede hata veriyor (ölçüldü):

```sql
SELECT id, name AS path ...                -- baslangic
SELECT e.id, c.path + N' > ' + e.name ...  -- kendini cagiran parca
```

`Types don't match between the anchor and the recursive part in column
"path" of recursive query "chain".`

`name` sütunu `NVARCHAR(40)`; birleştirilmiş yol daha uzun bir tip.
Sunucu iki parçada aynı tipi istiyor. Çare ikisini de aynı tipe
çevirmek:

```sql
SELECT id, CAST(name AS NVARCHAR(200)) AS path ...
SELECT e.id, CAST(c.path + N' > ' + e.name AS NVARCHAR(200)) ...
```

| id | path |
|---|---|
| 1 | Ada Kilic |
| 2 | Ada Kilic > Bora Yilmaz |
| 3 | Ada Kilic > Bora Yilmaz > Ceren Aksoy |
| 6 | Ada Kilic > Emre Sahin > Fulya Demir |

## Yukarı doğru

Aynı yapı ters yönde de çalışıyor. Fulya'dan en tepeye:

```sql
WITH up AS (
    SELECT id, name, manager_id, 0 AS step
    FROM employees WHERE id = 6
    UNION ALL
    SELECT e.id, e.name, e.manager_id, u.step + 1
    FROM employees e
    JOIN up u ON e.id = u.manager_id
)
SELECT step, name FROM up ORDER BY step;
```

Sonuç: Fulya Demir (0), Emre Sahin (1), Ada Kilic (2). Fark yalnızca
birleştirmede: aşağı inerken `e.manager_id = c.id` ("yöneticisi
zincirde olanlar"), yukarı çıkarken `e.id = u.manager_id` ("zincirdekinin
yöneticisi"). Yön ters yazılınca aşağı inen sorgu yalnızca Ada'yı
getirdi.

## Sonsuz döngüye karşı: MAXRECURSION

Durma koşulu olmayan bir özyineleme sonsuza kadar sürerdi. Sunucu
varsayılan olarak **100 adımda** kesiyor. 1'den başlayıp birer artan bir
sayaçla ölçüldü:

| Sorgu | Sonuç |
|---|---|
| `... WHERE k < 101` | 101 satır |
| `... WHERE k < 102` | `The statement terminated. The maximum recursion 100 has been exhausted before statement completion.` |
| `... WHERE k < 200` + `OPTION (MAXRECURSION 200)` | 200 satır |
| `... WHERE k < 1000` + `OPTION (MAXRECURSION 0)` | 1000 satır — `0` sınırı kaldırıyor |
| `OPTION (MAXRECURSION 40000)` | hata: en fazla 32767 |
| `WHERE` yok + `OPTION (MAXRECURSION 50)` | 50'de hata ile durdu |

`OPTION` CTE'nin içine değil, onu kullanan **cümlenin en sonuna**
yazılıyor; içine yazılınca sözdizimi hatası verdi. Sınır bir güvenlik
ağı: gerçek bir ağaç 100 kat derin olmaz, 100'ü aşan bir yönetim zinciri
büyük ihtimalle verideki bir hatadır.

## Hiçbir tabloda olmayan satırlar

Aylık ciro yalnızca siparişi olan ayları gösterir. "Ocak'tan Haziran'a
her ay" gerekiyorsa, aylar önce üretiliyor:

```sql
WITH months AS (
    SELECT CAST('2026-01-01' AS DATE) AS month
    UNION ALL
    SELECT DATEADD(month, 1, month)
    FROM months
    WHERE month < '2026-06-01'
),
revenue AS (
    SELECT DATEFROMPARTS(YEAR(o.order_date), MONTH(o.order_date), 1) AS month,
           SUM(i.quantity * i.unit_price) AS revenue
    FROM orders o
    JOIN order_items i ON i.order_id = o.id
    WHERE o.status <> 'cancelled'
    GROUP BY DATEFROMPARTS(YEAR(o.order_date), MONTH(o.order_date), 1)
)
SELECT m.month, COALESCE(r.revenue, 0) AS revenue
FROM months m
LEFT JOIN revenue r ON r.month = m.month
ORDER BY m.month;
```

| month | revenue |
|---|---|
| 2026-01-01 | 32715.00 |
| 2026-02-01 | 28680.00 |
| 2026-03-01 | 7710.00 |
| 2026-04-01 | 30060.00 |
| 2026-05-01 | **0.00** |
| 2026-06-01 | **0.00** |

İki ayrıntı sonucu değiştiriyor (ölçüldü): `LEFT JOIN` yerine `JOIN`
yazılınca Mayıs ve Haziran düştü (4 satır); `COALESCE` olmayınca o iki
ay `NULL` geldi.

## Özyinelemenin yasakları

Kendini çağıran parçada iki şey yazılamıyor (ölçüldü):

| Yazım | Hata |
|---|---|
| `MAX(k)`, `GROUP BY`, `HAVING` | `GROUP BY, HAVING, or aggregate functions are not allowed in the recursive part of a recursive common table expression` |
| `LEFT JOIN` | `Outer join is not allowed in the recursive part of a recursive common table expression` |

Toplama gerekiyorsa CTE'nin **dışında** yapılıyor. "Her çalışanın altında
(doğrudan ya da dolaylı) kaç kişi var?" — özyineleme her kök için
altındakileri listeliyor, sayma dışarıdaki `GROUP BY`'da:

```sql
WITH r AS (
    SELECT id AS root, id FROM employees
    UNION ALL
    SELECT r.root, e.id
    FROM employees e
    JOIN r ON e.manager_id = r.id
)
SELECT root, COUNT(*) - 1 AS below
FROM r
GROUP BY root;
```

Sonuç: Ada 5, Bora 2, Emre 1, geri kalanlar 0. (`- 1` kişinin kendisini
çıkarıyor.)

## WITH ile değiştirmek

CTE bir `SELECT`'in önüne yazılabildiği gibi `DELETE` ve `UPDATE`'in
önüne de yazılabiliyor — ve değişiklik **asıl tabloya** gidiyor.
Tekrarlanan kayıtları temizlemenin bilinen yolu:

```sql
WITH d AS (
    SELECT email,
           ROW_NUMBER() OVER (PARTITION BY email ORDER BY email) AS rn
    FROM #dup
)
DELETE FROM d WHERE rn > 1;
```

Altı satırlık bir tabloda (`a` iki, `b` bir, `c` üç kez) **3 satır**
silindi ve her adresten bir tane kaldı (ölçüldü). Aynı şekilde
`WITH cheap AS (SELECT TOP 2 ... ORDER BY price) UPDATE cheap SET stock =
stock + 100` en ucuz iki ürünün (Cable, Mouse) stoğunu `products`
tablosunda değiştirdi (ölçüm geri alınan bir işlemin içinde yapıldı).

## Özet

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">WITH ad AS (...)</span><span class="anat-body">Bir sorguya ad veriyor; ad yalnızca o cümle boyunca geçerli.</span></div>
    <div class="anat-row"><span class="anat-label">Birden fazla</span><span class="anat-body">Virgülle; her biri kendinden öncekileri görüyor.</span></div>
    <div class="anat-row"><span class="anat-label">Noktalı virgül</span><span class="anat-body"><code>WITH</code>'ten önceki cümle <code>;</code> ile bitmeli.</span></div>
    <div class="anat-row"><span class="anat-label">Özyineleme</span><span class="anat-body">Başlangıç + <code>UNION ALL</code> + kendini çağıran parça; yeni satır gelmeyince duruyor.</span></div>
    <div class="anat-row"><span class="anat-label">Tip</span><span class="anat-body">İki parçada sütun tipleri aynı olmalı: <code>CAST</code>.</span></div>
    <div class="anat-row"><span class="anat-label">Sınır</span><span class="anat-body">Varsayılan 100 adım; <code>OPTION (MAXRECURSION n)</code> cümlenin sonunda.</span></div>
  </div>
</figure>

Sıradaki bölüm dizinler: aynı sorgunun neden bazen yavaş çalıştığı ve
sunucunun bir satırı nasıl bulduğu.
