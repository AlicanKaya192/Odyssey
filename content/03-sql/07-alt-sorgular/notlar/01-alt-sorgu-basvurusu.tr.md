Alt sorgu biçimlerinin tek sayfalık özeti. Sonuçlar bu bölümün sekiz
tablolu şemasında ölçüldü.

## Nerede kullanılabiliyor

| Yer | Ne döndürmeli | Örnek |
|---|---|---|
| `WHERE` (karşılaştırma) | tek değer | `price > (SELECT AVG(price) ...)` |
| `WHERE` (`IN`) | tek sütun, çok satır | `code IN (SELECT ...)` |
| `WHERE` (`EXISTS`) | fark etmiyor | `EXISTS (SELECT 1 ...)` |
| `SELECT` | **tek satır, tek sütun** | `(SELECT COUNT(*) ...) AS n` |
| `FROM` | tablo — **takma adı zorunlu** | `FROM (SELECT ...) t` |
| `HAVING` | tek değer | `HAVING COUNT(*) > (SELECT ...)` |

`SELECT` içindeki alt sorgu birden fazla satır döndürürse hata:
`Subquery returned more than 1 value`.

## İlişkili mi değil mi

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">İlişkisiz</span><span class="anat-body">İçinde dış sorgunun takma adı <b>geçmiyor</b>. Bir kez çalışıyor, sonucu her satır için aynı. Tek başına da çalıştırılabiliyor.</span></div>
    <div class="anat-row"><span class="anat-label">İlişkili</span><span class="anat-body">İçinde dış sorgunun takma adı <b>geçiyor</b>. Dış sorgunun her satırı için yeniden çalışıyor. Tek başına çalıştırılamıyor.</span></div>
  </div>
</figure>

Ayırt etmenin pratik yolu: alt sorguyu kopyalayıp tek başına çalıştır.
Çalışıyorsa ilişkisiz, "invalid column name" diyorsa ilişkili.

## EXISTS ve NOT EXISTS

```sql
-- siparis vermis musteriler (5 satir)
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id)

-- hic siparis vermemis musteriler (1 satir)
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id)
```

Üç ayrıntı:

- **İçeride ne seçtiğinin önemi yok.** `SELECT 1`, `SELECT *`,
  `SELECT name` — hepsi aynı. Gelenek `1` yazmak.
- **Erken çıkıyor.** Bir satır bulunca duruyor; saymıyor.
- **Boş değerlerden etkilenmiyor.** `NOT IN`'in tuzağı burada yok.

## NOT IN tuzağı

Ölçüldü:

| Sorgu | Sonuç | Doğrusu |
|---|---|---|
| `code NOT IN (SELECT supplier_code FROM products)` | **0 satır** | 1 |
| `... WHERE supplier_code IS NOT NULL` eklenmiş | 1 satır | 1 |
| `NOT EXISTS (...)` | 1 satır | 1 |

Sebep: üç üründe `supplier_code` boş, yani listede `NULL` var. `NOT IN`
şu zincire dönüşüyor:

```
code <> 'S1' AND code <> 'S2' AND ... AND code <> NULL
                                          ^^^^^^^^^^^^ hep bilinmiyor
```

Bir `AND` zincirinde bilinmeyen bir parça varken sonuç asla doğru
olamıyor.

**Kural: alt sorguyla `NOT IN` yazma, `NOT EXISTS` yaz.**

Olumlu `IN` bu sorunu yaşamıyor: orada `OR` zinciri var ve bir parçanın
doğru olması yetiyor.

## Boş alt sorgu

| Sorgu | Sonuç |
|---|---|
| `IN (bos alt sorgu)` | hiç satır |
| `NOT IN (bos alt sorgu)` | **bütün satırlar** |
| `EXISTS (bos alt sorgu)` | hiç satır |
| `NOT EXISTS (bos alt sorgu)` | bütün satırlar |

Alt sorgu boş döndüğünde `NOT IN` güvenli — sorun yalnızca içinde `NULL`
olduğunda çıkıyor.

## Türetilmiş tablo

```sql
SELECT t.customer_id, t.order_count
FROM (
    SELECT customer_id, COUNT(*) AS order_count
    FROM orders GROUP BY customer_id
) t
WHERE t.order_count >= 2;
```

- **Takma ad zorunlu.** `) t` yazılmazsa sözdizimi hatası.
- İçerideki sorgunun her sütununa **ad verilmiş olmalı**; hesaplanan
  sütunlar `AS` ile adlandırılıyor.
- Basit durumlarda `HAVING` daha kısa. Türetilmiş tablo, gruplama
  sonucunu **başka bir tabloyla birleştirmek** gerektiğinde tek yol.

## Alt sorgu mu JOIN mi

| İhtiyaç | Tercih |
|---|---|
| Başka tablodan sütun getirmek | `JOIN` |
| Yalnızca süzmek | `EXISTS` / `IN` |
| Eşleşmeyeni bulmak | `NOT EXISTS` |
| Tek bir sayı (ortalama, toplam) | skaler alt sorgu |
| Gruplayıp sonra birleştirmek | türetilmiş tablo |

Hız açısından ikisi genelde aynı: sunucu çoğu alt sorguyu birleştirmeye
çevirebiliyor. Tek gerçek fark satır çoğalması — `JOIN` çoğaltabiliyor,
`EXISTS` çoğaltmıyor.
