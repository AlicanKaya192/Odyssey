## Dört tür

| Tür | Grafikte | Örnek | Ne yapılır |
|---|---|---|---|
| Tekil sıçrama | Tek nokta yukarıda ya da aşağıda, ertesi gün normal | Kampanya günü, kesinti, yazım hatası | Düzelt ya da işaretle |
| Geçici değişim | Sıçrama, sonra birkaç günde sönerek normale dönüş | Haber etkisi, stok tükenmesi sonrası toparlanma | Dönemi işaretle |
| Seviye kayması | Bir günden sonra her şey yeni düzeyde | Fiyat değişimi, yeni şube, ölçüm yöntemi değişti | Aykırı değer değil: değişim noktası |
| Mevsimsel olay | Her yıl aynı tarihte tekrar eden sıçrama | Bayram, yılbaşı, indirim haftası | Dokunma; takvim değişkeni |

Aynı sayı, türüne göre bambaşka bir işlem ister. **Önce türünü belirle.**

## Bulma yöntemleri

| Yöntem | Kod | Güçlü yanı | Zayıf yanı |
|---|---|---|---|
| z-skoru | `(x - x.mean()) / x.std()` | Basit | Aykırı değerler ölçüyü şişirir (maskeleme) |
| Dayanıklı z | `0.6745 * (x - med) / mad` | Uç değerden etkilenmez | Ham seride mevsimi aykırı sanar |
| Çeyrekler arası | `q1 - 1.5 * iqr`, `q3 + 1.5 * iqr` | Dağılım varsayımı yok | Trendli seride işe yaramaz |
| Hareketli z | `shift(1).rolling(28)` ile taban | Yerel düzeye uyar | Pencere seçimi; mevsimi bilmez |
| Hampel süzgeci | Hareketli ortanca ve MAD | Yerel ve dayanıklı | Haftalık desende hafta sonlarını işaretler |
| STL kalıntısı | `STL(..., robust=True).fit().resid` | Trend ve mevsim çıkarılmış | En az iki mevsim turu gerekir |

Mevsimli seride sıra: **dayanıklı STL → kalıntı → dayanıklı z → sırala.**

## MAD

```python
median = x.median()
mad = (x - median).abs().median()
robust_z = 0.6745 * (x - median) / mad
```

- Ortanca: verinin yarısı altında, yarısı üstünde.
- MAD: ortancadan sapmaların ortancası. Verinin %49'u saçma olsa bile
  bozulmaz.
- `mad == 0` olabilir (değerlerin yarısından fazlası aynıysa): bölmeden önce
  denetle.

Normal dağılan veride `mad / 0.6745 ≈ std`. Bu yüzden 0.6745 ile çarpınca
bildiğin z-skoru ölçeğine geliyor.

## Hampel süzgeci

Kayan pencerede dayanıklı z:

```python
window = 15
med = x.rolling(window, center=True, min_periods=window // 2).median()
mad = (x - med).abs().rolling(window, center=True, min_periods=window // 2).median()
score = 0.6745 * (x - med) / mad
flagged = score.abs() > 3.5
```

Mevsimi olmayan sensör verisinde çok iyi çalışır. Haftalık deseni olan seride
her hafta sonunu işaretler; önce deseni çıkar.

## Eşik

| Eşik | Normal dağılımda şans eseri aşma |
|---|---|
| 2 | 20 gözlemde 1 |
| 3 | 370 gözlemde 1 |
| 3.5 | 2150 gözlemde 1 |
| 4 | 15800 gözlemde 1 |

Gerçek kalıntılar normal dağılmaz; kuyrukları kalındır ve aynı eşik çok daha
fazla günü işaretler. Pratik yol:

1. Puanları büyükten küçüğe sırala.
2. İlk 10–20'sine bak: doğal bir kopma var mı?
3. İşaretlenen günleri takvimle karşılaştır: tatil, kampanya, bilinen arıza.
4. Açıklayamadığın günleri ayrıca not et.

## Düzeltme seçenekleri

| Seçenek | Kod | Ne zaman |
|---|---|---|
| Eksik say ve doldur | `x[days] = nan`, sonra mevsimsel doldurma | Hata ya da tek seferlik olay |
| Kırp | `x.clip(lower, upper)` | Çok sayıda hafif uç değer; yönü koru, boyu sınırla |
| Beklenenle değiştir | `trend + seasonal` (STL'den) | Tutarlı, model tabanlı düzeltme |
| İşaret sütunu | `is_event = x.index.isin(days)` | Olay gerçek; modele anlat |
| Dokunma | | Tekrar eden olay; dayanıklı yöntem kullan |

Hangi seçeneği kullanırsan kullan: **özgün seri ayrı sütunda kalır** ve
dokunduğun günlerin listesi tutulur.

## Aykırı değere dayanıklı araçlar

Bazen düzeltmek yerine etkilenmeyen bir araç seçmek yeter:

| Hassas | Dayanıklı |
|---|---|
| Ortalama | Ortanca |
| Standart sapma | MAD, çeyrekler arası aralık |
| `rolling().mean()` | `rolling().median()` |
| `seasonal_decompose` | `STL(..., robust=True)` |
| Ortalama kare hata (Bölüm 15) | Ortalama mutlak hata |

## Aykırı değer bazen asıl konudur

Dolandırıcılık tespiti, arıza erken uyarısı, siber saldırı izleme: bu işlerde
aykırı değer gürültü değil, **aradığın şey**. Aynı araçlar, ters amaçla.
Bölüm 21 bu konuya ayrılmış.
