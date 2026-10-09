## Algoritma

1. `k` merkez seç (k-means++ ile).
2. **Ata:** her nokta en yakın merkeze.
3. **Güncelle:** her merkez kendi noktalarının ortalaması.
4. Merkezler durana kadar 2–3.

Bir turun maliyeti `n · k · d` (nokta × merkez × özellik); büyük veride
bile hızlıdır.

## Ölçütler

| Ne | Tanım | İyi |
|---|---|---|
| Inertia | `Σ ‖x − merkez(x)‖²` | küçük, ama `k` arttıkça hep düşer |
| Siluet | `s = (b − a) / max(a, b)` | 1'e yakın |
| Düzeltilmiş Rand | bulunan kümeler ile gerçek gruplar | 1 (yalnızca etiket varsa) |

Siluette `a` noktanın kendi kümesindeki noktalara ortalama uzaklığı, `b` en
yakın başka kümeye ortalama uzaklığı.

## scikit-learn

| Parametre | Anlamı |
|---|---|
| `n_clusters` | `k` |
| `init` | `"k-means++"` (varsayılan) ya da `"random"` ya da dizi |
| `n_init` | kaç başlangıç; en düşük inertia tutulur |
| `max_iter` | tur sınırı |

Sonuçlar: `cluster_centers_`, `labels_`, `inertia_`, `n_iter_`; yeni nokta
için `predict`.

## Sık hatalar

- Ölçeklememek: büyük birimli özellik uzaklığı tek başına belirler.
- `k`'yı inertia'nın en küçük olduğu yerde seçmek: o hep en büyük `k`.
- Tek başlangıçla yetinmek: yerel minimum.
- Boş küme: hiç nokta almayan merkezin ortalaması hesaplanamaz; scikit-learn
  o merkezi en uzak noktaya taşır, elle yazılan sürüm bunu düşünmeli.
- Kategorik veriye uygulamak: ortalama anlamsız (k-modes gibi türler var).
