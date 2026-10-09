Algoritmalarda logaritma çok sık çıkar ve çoğu zaman tek bir sorunun
cevabıdır: **"Bir sayıyı 1'e inene kadar kaç kez ikiye bölebilirim?"**

| `n` | Kaç kez yarıya | `log₂ n` (yaklaşık) |
|---|---|---|
| 8 | 8 → 4 → 2 → 1: 3 kez | 3 |
| 1 024 | 10 kez | 10 |
| 1 000 000 | 19–20 kez | 19,9 |
| 1 000 000 000 | 29–30 kez | 29,9 |

Bir başka bakış: `log₂ n`, `n`'nin ikili (binary) gösteriminde kabaca kaç
basamak olduğu. 1 024 ikili yazılınca 11 basamak (`10000000000`).

## Algoritmada nereden çıkar?

- **Her adımda aramanın yarısını eleyen** algoritmalar: ikili arama. Bir
  milyon kayıtta en fazla 20 karşılaştırma.
- **Ağaçlar:** dengeli bir ikili ağacın yüksekliği `log₂ n`. Bir milyon
  elemanlı dengeli ağaçta kökten yaprağa 20 adım.
- **Böl ve fethet:** listeyi ikiye bölüp her yarıyı ayrı çözen algoritmalar
  (merge sort) `log₂ n` kat derinliğe iner; her katta `n` iş yapınca
  `O(n log n)`.

## Tabanın önemi yok

`log₂ n`, `log₁₀ n` ve `ln n` birbirinin sabit katıdır
(`log₂ n ≈ 3,32 × log₁₀ n`). Büyük O sabitleri attığı için tabanı yazmayız:
yalnızca `O(log n)` deriz.

## Hissetmek için

Bir telefon rehberinde (sıralı) bir adı ararken ortadan açıp "daha ileride
mi, geride mi?" diye bakarsın. 1 000 sayfalık rehberde en fazla 10 kez
açman yeter. Rehber 1 000 000 sayfa olsaydı 20 kez. Sayfa sayısı bin kat
arttı, iş yalnızca iki katına çıktı.

Logaritmanın matematiği Temel Matematik modülünün **Logaritma** bölümünde.
