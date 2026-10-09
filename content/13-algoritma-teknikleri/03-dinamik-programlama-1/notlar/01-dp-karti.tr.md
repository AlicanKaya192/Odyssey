## Tarif

1. **Durum:** tablonun bir hücresi neyi gösteriyor?
2. **Geçiş:** bir hücre küçük hücrelerden nasıl hesaplanıyor?
3. **Taban:** en küçük hücrelerin değeri.
4. **Sıra:** ihtiyaç duyulan hücreler önce dolacak şekilde.
5. **Cevap:** hangi hücre?

## Yukarıdan aşağı mı, aşağıdan yukarı mı?

| | Bellekli özyineleme | Tablo doldurma |
|---|---|---|
| Yazması | özyineli çözüme bir sözlük ya da `@cache` eklemek | sırayı düşünmek gerekir |
| Hesaplanan | yalnızca gereken alt problemler | bütün tablo |
| Derinlik | özyineleme sınırına takılabilir | sorun yok |
| Bellek küçültme | zor | kolay (yalnızca son satırlar) |

Derinlik sınırı gerçek bir sorun:

```python
from functools import cache

@cache
def fib_memo(n):
    return n if n < 2 else fib_memo(n - 1) + fib_memo(n - 2)

try:
    fib_memo(5000)
except RecursionError:
    print("RecursionError")

def fib_table(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print(len(str(fib_table(5000))), "digits")
```

```text
RecursionError
1045 digits
```

## Sık görülen biçimler

| Biçim | Örnek | Durum |
|---|---|---|
| Tek boyut, önceki birkaç hücre | Fibonacci, merdiven | `dp[i]` |
| Tek boyut, bütün seçenekler | en az para | `dp[tutar]` |
| Tek geçiş, "burada biten" | Kadane | `current` |
| İki boyut, üst ve sol | ızgarada yollar | `dp[r][c]` |
| İki dizi | en uzun ortak alt dizi, düzenleme uzaklığı | `dp[i][j]` (DP 2) |
| Eşya × kapasite | 0/1 sırt çantası | `dp[i][w]` (DP 2) |

## Sık hatalar

- Taban durumunu yanlış koymak: kaç yol sorusunda `ways[0] = 1` (hiç para
  vermemek bir yol), en az para sorusunda `best[0] = 0`.
- "Kaç yol" sorusunda döngü sırasını karıştırmak: paralar dışta →
  kombinasyon, tutarlar dışta → sıralanış.
- Ulaşılamayan durumu 0 sanmak: en az para sorusunda başlangıç değeri
  `inf`; sonda hâlâ `inf` ise o tutar verilemez.
- `@cache` ile listeyi argüman vermek: liste hash'lenemez, `TypeError`; demet
  ver.
