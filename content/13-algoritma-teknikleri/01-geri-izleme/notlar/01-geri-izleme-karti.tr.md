## İskelet

```python
result, path = [], []

def backtrack(DURUM):
    if TAMAM_MI:
        result.append(path[:])        # kopya!
        return
    for choice in SECENEKLER:
        if ISE_YARAMAZ(choice):       # budama
            continue                  # ya da sıralıysa: break
        path.append(choice)           # seç
        backtrack(YENI_DURUM)         # keşfet
        path.pop()                    # geri al
```

## Kaç olasılık var?

| Problem | Sayı | `n = 10` | Hazırı |
|---|---|---|---|
| Alt kümeler | `2ⁿ` | 1024 | `combinations(items, k)` her `k` için |
| Sıralanışlar | `n!` | 3 628 800 | `permutations(items)` |
| `k` elemanlı seçimler | `n! / (k!(n−k)!)` | `k = 3`: 120 | `combinations(items, k)` |
| Her konuma `m` seçenek | `mⁿ` | `m = 3`: 59 049 | `product(seçenekler, repeat=n)` |

## Budama için sorular

- Sıralı veride bir sınırı aştıysam, sonrakiler de aşar mı? → `break`.
- Bu seçim bir kuralı bozuyor mu (aynı sütun, aynı sayı)? → `continue`.
- Kalan seçeneklerin en iyisi bile şimdiki en iyiyi geçemez mi? → dön
  (dal ve sınır, branch and bound).
- Aynı değer iki kez varsa aynı dalı iki kez açıyor muyum? → sıralayıp
  `if i > start and items[i] == items[i - 1]: continue`.

## Sık hatalar

- `result.append(path)`: hepsi aynı listeye bakar, sonunda boş kalır.
  `path[:]` ya da `list(path)` yaz.
- Geri alırken yalnızca `path.pop()` yapıp `used[i] = False` ya da kümeden
  silmeyi unutmak → sonraki dallar yanlış kısıtla çalışır.
- Varsayılan değer olarak liste: `def f(path=[])` bütün çağrılarda aynı
  listeyi paylaşır.
- Budamayı sıralamadan `break` ile yapmak: sıralı değilse sonraki eleman
  daha küçük olabilir, çözümler kaybolur.
