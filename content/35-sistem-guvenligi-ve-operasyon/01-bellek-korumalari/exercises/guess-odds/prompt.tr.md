İki fonksiyon yaz:

- `guess_odds(bits)`: `"1 in <sayi>"` metni; sayı `2 ** bits`, binlik
  ayraçla (`f"{n:,}"`): `guess_odds(16)` → `"1 in 65,536"`.
- `average_tries(bits)`: ortalama deneme sayısı, olası adreslerin yarısı:
  `2 ** (bits - 1)`.

**Beklenen çıktı:**

```
8: 1 in 256
  average 128
16: 1 in 65,536
  average 32768
28: 1 in 268,435,456
  average 134217728
```
