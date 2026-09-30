## Fikir

Üstel ağırlıklı ortalama her adımda tek bir kural uyguluyor:

```text
yeni ortalama = alpha × bugünkü değer + (1 - alpha) × dünkü ortalama
```

`alpha` 0 ile 1 arasında: bugüne ne kadar ağırlık verildiği. Dünkü ortalama
da aynı kuralla hesaplandığı için bütün geçmiş işin içinde, ama her adım
geriye gidildikçe ağırlık `(1 - alpha)` ile çarpılarak küçülüyor.

`alpha = 0.25` için ağırlıklar:

| Kaç gün önce | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| Ağırlık | 0.250 | 0.188 | 0.141 | 0.105 | 0.079 | 0.059 | 0.044 | 0.033 |

Son 7 günün toplam ağırlığı 0.867. Kalan 0.133 daha eski günlere yayılmış:
hiçbir gün tam olarak unutulmuyor, yalnızca sesi kısılıyor.

## Ağırlığı söylemenin üç yolu

| Parametre | `alpha` karşılığı | Okunuşu |
|---|---|---|
| `alpha=0.25` | 0.25 | Doğrudan ağırlık |
| `span=7` | `2 / (span + 1)` = 0.25 | "7 günlük hareketli ortalamaya benzer" |
| `halflife=2.4` | `1 - 0.5 ** (1 / halflife)` | Ağırlığın yarıya indiği adım sayısı |
| `com=3` | `1 / (1 + com)` = 0.25 | Kütle merkezi |

Dördü aynı şeyi anlatıyor; yalnızca biri verilir. `span` en sık kullanılanı,
çünkü hareketli ortalamayla karşılaştırması kolay.

| `span` | `alpha` | Davranış |
|---|---|---|
| 2 | 0.667 | Çok hızlı, neredeyse ham seri |
| 7 | 0.250 | Dengeli |
| 28 | 0.069 | Yavaş, çok düz |
| 365 | 0.005 | Çok yavaş; trende yakın |

## `adjust` parametresi

```python
s.ewm(span=7).mean()                  # adjust=True (varsayilan)
s.ewm(span=7, adjust=False).mean()    # yukaridaki kuralin birebir kendisi
```

- **`adjust=True`**: baştaki satırlarda elindeki az sayıda değerin
  ağırlıklarını toplamı 1 olacak şekilde düzeltiyor. İlk değerler daha dengeli
  başlıyor.
- **`adjust=False`**: yukarıdaki tekrarlı kuralı olduğu gibi uyguluyor; ilk
  ortalama ilk değerin kendisi.

Seri uzadıkça ikisi aynı sonuca yaklaşıyor. Kitaplardaki "basit üstel
düzleştirme" formülü `adjust=False`.

## Hareketli ortalama ile karşılaştırma

| | `rolling(n).mean()` | `ewm(span=n).mean()` |
|---|---|---|
| Ağırlıklar | Pencerede eşit, dışında sıfır | Yumuşakça azalıyor |
| Baştaki satırlar | `NaN` | Dolu |
| Seviye değişimine tepki | Pencere dolana kadar doğrusal | İlk adımda büyük, sonra yavaşlayan |
| Eski aykırı değer | Pencereden **birden** çıkıyor | Yavaşça sönüyor |
| Mevsimselliği bastırma | Pencere mevsime eşitse **tam** | Yalnızca kısmen |
| Hesap için gereken | Son n değer | Yalnızca bir önceki ortalama |

**Mevsimsellik satırı önemli.** 7 günlük hareketli ortalama haftalık deseni
tamamen yok ediyor, çünkü pencerede her günden tam bir tane var. `ewm` en
yeni güne daha çok ağırlık verdiği için cumartesi günü yukarı, pazartesi günü
aşağı kayıyor. Mevsimselliği temizlemek için hareketli ortalama, hızlı tepki
veren bir seviye tahmini için `ewm`.

## Üstel ağırlıklı oynaklık

```python
r = close.pct_change()
vol = r.ewm(span=20).std()
```

Eşit ağırlıklı 20 günlük oynaklıkta büyük bir hareket 20 gün boyunca aynı
ağırlıkla duruyor, 21. gün birden kayboluyor. Üstel ağırlıklı oynaklık o
günün etkisini yavaşça azaltıyor; risk ölçümünde bu yüzden yaygın.

## Tahmine köprü

`ewm` ile hesaplanan ortalamanın **son değeri**, yarın için yapılabilecek en
basit tahminlerden biri: "seviye şu an burada". Bu yönteme **basit üstel
düzleştirme** deniyor. Trend eklenince Holt, mevsimsellik de eklenince
Holt-Winters oluyor; üçü de Bölüm 16'da.

`alpha`'nın anlamı orada da aynı:

- **Büyük `alpha`**: yeni veriye çabuk uyum, ama gürültüye de tepki veriyor.
- **Küçük `alpha`**: sakin, ama gerçek bir değişimi geç fark ediyor.
