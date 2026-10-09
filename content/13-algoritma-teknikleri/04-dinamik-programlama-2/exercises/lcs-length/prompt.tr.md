`lcs_length(a, b)` fonksiyonunu yaz: iki metnin en uzun ortak alt dizisinin
(aynı sırada, yan yana olması gerekmeyen) **uzunluğunu** döndürsün.

Eşleşirse `dp[i − 1][j − 1] + 1`, değilse `max(dp[i − 1][j], dp[i][j − 1])`.

Son satırda 1500 harflik iki metin var; bütün alt dizileri denemek imkânsız,
tablo 2,25 milyon hücre.

**Beklenen çıktı:**

```
4
5
750
```
