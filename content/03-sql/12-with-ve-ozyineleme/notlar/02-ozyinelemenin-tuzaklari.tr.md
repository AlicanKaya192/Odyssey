Özyinelemeli bir sorgu yazarken düşülen tuzakların bir kısmı hata
veriyor, bir kısmı sessizce yanlış sonuç. Bu not, bu bölümde ölçülenleri
ve her birinin çaresini topluyor.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Ters yön</span><span class="anat-body">Birleştirmenin hangi sütundan hangisine gittiğini kontrol et.</span></div>
    <div class="anat-row"><span class="anat-label">Tip</span><span class="anat-body">Metin biriktirirken iki parçada da <code>CAST</code>.</span></div>
    <div class="anat-row"><span class="anat-label">Durma koşulu</span><span class="anat-body">Kendini çağıran parçada bir <code>WHERE</code> ya da biten bir birleştirme.</span></div>
    <div class="anat-row"><span class="anat-label">Sınır</span><span class="anat-body">100'ü aşacaksan <code>OPTION (MAXRECURSION n)</code>, cümlenin sonunda.</span></div>
    <div class="anat-row"><span class="anat-label">Toplama</span><span class="anat-body">Özyinelemenin içinde değil, dışında.</span></div>
    <div class="anat-row"><span class="anat-label">Noktalı virgül</span><span class="anat-body"><code>WITH</code>'ten önceki cümleyi <code>;</code> ile bitir.</span></div>
  </div>
</figure>

## 1. Ters yön — hata yok, satır eksik

Aşağı inen kademe sorgusunda birleştirme `e.manager_id = c.id` olmalı:
"yöneticisi zincirde olan çalışanlar". Ters yazılınca
(`e.id = c.manager_id`) sorgu **hata vermeden** yalnızca Ada'yı getirdi:
Ada'nın yöneticisi yok, zincire kimse eklenmedi, özyineleme ilk adımda
bitti.

| Yön | Birleştirme | Ölçülen |
|---|---|---|
| aşağı (kimin altında kim var) | `e.manager_id = c.id` | 6 çalışan |
| yukarı (kimin üstünde kim var) | `e.id = c.manager_id` | Fulya → Emre → Ada |

**Çare:** yüksek sesle oku — "zincirdekinin **yöneticisi**" mi, "yöneticisi
**zincirde** olan" mı?

## 2. Tip uyuşmazlığı

Başlangıçta `name` (`NVARCHAR(40)`), kendini çağıran parçada
`c.path + N' > ' + e.name` (daha uzun bir tip):

`Types don't match between the anchor and the recursive part in column
"path" of recursive query "chain".`

Aynı şey sayılarda da olur: başlangıçta `0` (`INT`), sonra
`c.total + x.price` (`DECIMAL`) yazılırsa iki parça farklı tipte kalır.

**Çare:** iki parçada da aynı `CAST`: `CAST(... AS NVARCHAR(200))`.
Uzunluğu en uzun zincire yetecek kadar seç.

## 3. Durma koşulu ve sınır

Sayaç ya da tarih üreten bir özyinelemede durma koşulunu sen yazıyorsun
(`WHERE k < 200`, `WHERE month < '2026-06-01'`). Unutulursa sunucu
sınırda kesiyor:

| Durum | Ölçülen |
|---|---|
| varsayılan sınır | 101 satır geçti, 102'de `The maximum recursion 100 has been exhausted` |
| `OPTION (MAXRECURSION 200)` | 200 satır |
| `OPTION (MAXRECURSION 0)` | sınırsız — 1000 satır |
| `WHERE` yok, `MAXRECURSION 50` | 50'de hata ile durdu |

Ağaçta durma koşulu kendiliğinden var: altında kimse olmayan çalışanda
birleştirme boş dönüyor.

**Çare:** üretilen dizilerde koşulu en başta yaz; sınırı kaldırmak
(`0`) yalnızca koşulun doğru olduğundan eminken.

## 4. OPTION'ın yeri

`OPTION (MAXRECURSION n)` CTE'nin içine yazılınca `Incorrect syntax near
the keyword 'OPTION'` verdi. Yeri, CTE'yi kullanan **cümlenin sonu**:

```sql
WITH n AS (...)
SELECT COUNT(*) FROM n
OPTION (MAXRECURSION 200);
```

## 5. Özyinelemenin içinde toplama

Kendini çağıran parçada `MAX`, `GROUP BY`, `HAVING` (hata 467) ve `LEFT
JOIN` (hata 462) yazılamıyor.

**Çare:** özyineleme yalnızca satırları üretsin; sayma ve toplama
dışarıda. Alt çalışan sayısı böyle ölçüldü: özyineleme her kök için
altındakileri listeledi, dıştaki `GROUP BY root` saydı (Ada 5, Bora 2,
Emre 1).

## 6. UNION ALL, UNION değil

`UNION` yazılınca hata: `does not contain a top-level UNION ALL
operator`. Tekrarları ayıklamak gerekiyorsa bu da dışarıda (`DISTINCT`)
yapılıyor.

## 7. Noktalı virgül

Bu bölümün en sık hatası özyinelemeyle ilgili değil, `WITH`'in kendisiyle
ilgili: önceki cümle `;` ile bitmezse iki farklı mesajdan biri geliyor.
Mesajların ikisi de sonunda aynı şeyi söylüyor — önceki cümleyi bitir.

## Kontrol sorusu

Özyinelemeli bir sorgu yazınca üç şey sor:

- **"Başlangıçta hangi satırlar var?"** — `UNION ALL`'dan önceki sorguyu
  tek başına çalıştır.
- **"Her adımda kim ekleniyor?"** — birleştirmenin yönünü oku.
- **"Ne zaman duruyor?"** — ağaçta veri, dizide senin `WHERE`'in.
