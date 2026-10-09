## Python'da hazır olanlar

| Ne | Nasıl | Not |
|---|---|---|
| EBOB / EKOK | `math.gcd(a, b)`, `math.lcm(a, b)` | `math.lcm(4, 6)` = 12 |
| Tam karekök | `math.isqrt(n)` | büyük sayıda `int(n ** 0.5)` yanılabilir |
| Mod ile üs | `pow(a, e, m)` | hızlı üs alma |
| Mod tersi | `pow(a, -1, m)` | `pow(3, -1, 7)` = 5, çünkü `3 × 5 % 7 = 1` |
| Bölüm ve kalan | `divmod(a, b)` | `divmod(17, 5)` = `(3, 2)` |

## Maliyetler

| Algoritma | Maliyet |
|---|---|
| Öklid | `O(log min(a, b))` |
| Asallık (kareköke kadar) | `O(√n)` |
| Kalbur (`n`'e kadar bütün asallar) | `O(n log log n)` zaman, `O(n)` bellek |
| Hızlı üs alma | `O(log e)` çarpma |

## Sık hatalar

- Kayan noktalı karekök: `n = (10**8 + 1)**2 - 1` için `int(n ** 0.5)`
  100000001 veriyor, doğrusu 100000000 (`math.isqrt`).
- Önce dev sayıyı hesaplayıp sonra mod almak: `3 ** 1_000_000 % m` doğru ama
  yüz binlerce basamaklı bir ara sayı kurar; `pow(3, 1_000_000, m)` kurmaz.
- Negatif sayının modu: Python'da `-7 % 3` = 2 (sonuç hep `0`..`m − 1`);
  başka dillerde `-1` çıkabilir.
- Kalburda iç döngüyü `2 * p`'den başlatmak yanlış değil ama gereksiz:
  `p * p`'den küçük katlar daha küçük asallarca zaten işaretlendi.
