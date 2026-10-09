## Hangi yöntem?

| Yöntem | Maliyet | Ne zaman? |
|---|---|---|
| Saf arama | `O(n · m)` kötü durumda | kısa kalıp, tek arama |
| KMP | `O(n + m)` | kalıp kendini tekrar ediyor, kötü durum önemli |
| Rabin-Karp | ortalama `O(n + m)` | çok kalıp, kopya parça bulma |
| Trie | önek boyu kadar | önek araması, otomatik tamamlama |
| Python `in`, `str.find` | C ile yazılmış | tek kalıp için ilk tercih |

## KMP önek tablosu

`table[i]`: `pattern[:i + 1]`'in hem öneki hem soneki olan en uzun parçanın
boyu (parçanın kendisi hariç).

| Kalıp | Tablo |
|---|---|
| `abacab` | `0 0 1 0 1 2` |
| `aaaa` | `0 1 2 3` |
| `abcd` | `0 0 0 0` |

## Kayan hash

- Yeni pencere = (eski − çıkan harf × `base^(m−1)`) × `base` + giren harf,
  hepsi `mod` ile.
- Eşit hash **eşleşme demek değildir**: harfleri ayrıca karşılaştır.
- `mod` büyük bir asal seçilir; küçük `mod` çakışmayı artırır.

## Sık hatalar

- Saf aramada döngüyü `len(text) - len(pattern) + 1`'e kadar değil
  `len(text)`'e kadar kurmak: metin dışına taşan indeks.
- KMP'de eşleşme bulunca `k`'yı sıfırlamak: üst üste binen eşleşmeler
  (`"aaa"` içinde `"aa"` iki kez) kaçar; doğrusu `k = table[k - 1]`.
- Rabin-Karp'ta hash eşitliğini doğrudan eşleşme saymak.
- Trie'de kelime sonunu işaretlememek: `data` eklenip `dat` sorulunca `dat`
  da kelime sanılır.
