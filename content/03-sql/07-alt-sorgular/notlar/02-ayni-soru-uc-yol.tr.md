Aynı soruyu üç farklı yoldan sorabiliyorsun. Bu not hangisini ne zaman
seçeceğini gösteriyor — üçü de bu bölümün şemasında ölçüldü.

## Soru: hiç siparişi olmayan müşteriler

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">NOT EXISTS</span><span class="anat-body"><b>Tercih edilen.</b> Niyeti doğrudan söylüyor, boş değerlerden etkilenmiyor, satır çoğaltmıyor.</span></div>
    <div class="anat-row"><span class="anat-label">LEFT JOIN + IS NULL</span><span class="anat-body">Çalışıyor ve yaygın. İki adımlı olduğu için ilk bakışta ne sorduğu daha az belli.</span></div>
    <div class="anat-row"><span class="anat-label">NOT IN</span><span class="anat-body"><b>Kaçınılan.</b> Listede tek bir boş değer varsa sessizce boş sonuç veriyor.</span></div>
  </div>
</figure>

```sql
-- 1. NOT EXISTS
SELECT c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);

-- 2. LEFT JOIN
SELECT c.name FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;

-- 3. NOT IN  (bu veride calisiyor cunku customer_id hic bos degil,
--             ama supplier_code'da ayni yazim bos sonuc veriyor)
SELECT name FROM customers
WHERE id NOT IN (SELECT customer_id FROM orders);
```

Üçü de bu veride aynı sonucu veriyor. Ama üçüncüsü **verinin şu anki
hâline** bağlı: `orders.customer_id` bir gün boş olabilen bir sütuna
dönüşürse sorgu sessizce bozuluyor.

**Kural: olumsuz soru soruyorsan `NOT EXISTS` yaz.**

## Soru: her müşterinin sipariş sayısı

```sql
-- 1. LEFT JOIN + GROUP BY
SELECT c.name, COUNT(o.id) AS n
FROM customers c LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.name;

-- 2. skaler alt sorgu
SELECT c.name,
       (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.id) AS n
FROM customers c;
```

İkisi de aynı sonucu veriyor (altı satır, Quiet Partners için 0).

- **Tek bir sayı** ekleyeceksen alt sorgu daha okunur: `GROUP BY`
  yazmıyorsun ve gruplamanın diğer sütunlara etkisini düşünmüyorsun.
- **Birkaç sayı birden** ekleyeceksen `JOIN` + `GROUP BY` daha iyi: her
  biri için ayrı alt sorgu yazmak hem uzuyor hem tekrar ediyor.

## Soru: kendi grubunun ortalamasının üstündekiler

Bu soruyu bu bölümün araçlarıyla **yalnızca ilişkili alt sorgu**
çözebiliyor:

```sql
SELECT p.name FROM products p
WHERE p.price > (
    SELECT AVG(p2.price) FROM products p2
    WHERE p2.category_code = p.category_code);
```

`JOIN` ile çözmek için önce kategori ortalamalarını üreten bir türetilmiş
tablo kurup sonra onu birleştirmek gerekiyor:

```sql
SELECT p.name
FROM products p
JOIN (SELECT category_code, AVG(price) AS ort
      FROM products GROUP BY category_code) a
  ON a.category_code = p.category_code
WHERE p.price > a.ort;
```

İkincisi daha uzun ama büyük tablolarda genelde daha hızlı: ortalamalar
bir kez hesaplanıyor, her satır için yeniden değil.

İleri seviyede bunun üçüncü ve en okunur yolu var: **pencere
fonksiyonları**.

## Karar özeti

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Sütun getir</span><span class="anat-body"><code>JOIN</code></span></div>
    <div class="anat-row"><span class="anat-label">Var mı diye sor</span><span class="anat-body"><code>EXISTS</code></span></div>
    <div class="anat-row"><span class="anat-label">Yok mu diye sor</span><span class="anat-body"><code>NOT EXISTS</code> — <b>asla</b> <code>NOT IN</code></span></div>
    <div class="anat-row"><span class="anat-label">Tek sayı hesapla</span><span class="anat-body">skaler alt sorgu</span></div>
    <div class="anat-row"><span class="anat-label">Grupla sonra birleştir</span><span class="anat-body">türetilmiş tablo</span></div>
  </div>
</figure>

## Okunabilirlik notu

Alt sorgular iç içe geçtiğinde okunmaz hâle geliyor. Üç seviyeden fazla
iç içe yazıyorsan büyük ihtimalle sorguyu bölmen gerekiyor.

İleri seviyede bunun aracı var: `WITH` (ortak tablo ifadesi). Aynı işi
yapıyor ama yukarıdan aşağı, adlandırılmış adımlar hâlinde yazılıyor.
