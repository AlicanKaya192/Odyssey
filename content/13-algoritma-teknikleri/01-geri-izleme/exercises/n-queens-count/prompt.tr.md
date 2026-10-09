`count_queens(n)` fonksiyonunu yaz: `n × n` tahtaya birbirini tehdit
etmeyen `n` vezir kaç farklı şekilde dizilir, onu döndürsün.

Her satıra bir vezir koy; kullanılan sütunları ve iki çapraz yönünü
(`row - col`, `row + col`) üç kümede tut, tehdit altındaki kareyi hiç deneme.

Son satır `n = 11` (bütün sıralanışları denemek `11!` ≈ 40 milyon tahta)
için süre sınırı içinde bitmeli.

**Beklenen çıktı:**

```
4 2
6 4
8 92
11 2680
```
