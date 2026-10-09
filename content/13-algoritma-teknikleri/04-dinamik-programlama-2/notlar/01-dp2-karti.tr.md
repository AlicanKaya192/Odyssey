## İki boyutlu DP'ler

| Problem | Durum | Geçiş | Maliyet |
|---|---|---|---|
| 0/1 sırt çantası | `best[i][w]` | `max(best[i−1][w], best[i−1][w−ağırlık] + değer)` | `O(n · W)` |
| En uzun ortak alt dizi | `dp[i][j]` | eşleşirse `dp[i−1][j−1] + 1`, değilse `max(üst, sol)` | `O(n · m)` |
| Düzenleme uzaklığı | `dp[i][j]` | `min(üst + 1, sol + 1, çapraz + (eşit değilse 1))` | `O(n · m)` |
| En uzun artan alt dizi | `best[i]` | `max(best[j] + 1)`, `values[j] < values[i]` | `O(n²)`; `bisect` ile `O(n log n)` |
| DTW | `dp[i][j]` | `fark + min(üst, sol, çapraz)` | `O(n · m)` |

## Taban satırları

- LCS: ilk satır ve sütun 0 (boş metinle ortak bir şey yok).
- Düzenleme uzaklığı: `dp[i][0] = i` (hepsini sil), `dp[0][j] = j` (hepsini
  ekle).
- DTW: `dp[0][0] = 0`, kalan kenarlar sonsuz (bir seri boşken eşleşme yok).
- Sırt çantası: `best[0][w] = 0` (eşya yok).

## Geri çıkarma

Tablo yalnızca **en iyi değeri** tutar; seçimlerin kendisi için sondan geriye
yürünür. Her hücrede "bu değer hangi seçenekten geldi?" diye bakılır:

- Sırt çantası: üst satırla aynıysa eşya alınmamış, değilse alınmış.
- LCS: harfler eşitse o harf diziye girer, çapraza git; değilse büyük olan
  komşuya git.

Bellek küçültülmüş tabloda (yalnızca son satır) geri çıkarma yapılamaz.

## Sık hatalar

- İndeks kayması: tablo `len + 1` boyunda, metnin `i`'inci harfi `a[i − 1]`.
- Sırt çantasında aynı eşyayı iki kez almak: tek satırlı sürümde kapasite
  döngüsü **büyükten küçüğe** gitmeli (`for w in range(W, ağırlık − 1, −1)`);
  küçükten büyüğe giderse eşya tekrar tekrar alınır.
- LIS'te `tails` listesinin kendisini cevap sanmak: `tails` geçerli bir alt
  dizi olmayabilir, yalnızca **uzunluğu** doğrudur.
