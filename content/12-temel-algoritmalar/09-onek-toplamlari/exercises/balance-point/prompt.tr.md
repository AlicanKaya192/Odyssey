`balance_index(values)` fonksiyonunu yaz: solundaki elemanların toplamı
sağındakilerin toplamına eşit olan **ilk** indeksi döndürsün (o indeksteki
eleman iki tarafa da girmez); yoksa `-1`.

- `[1, 7, 3, 6, 5, 6]` → `3` (sol: 1 + 7 + 3 = 11, sağ: 5 + 6 = 11)

İç içe döngüye gerek yok: önce bütün toplamı bul. Listeyi gezerken sol
toplamı biriktir; sağ toplam `toplam - sol - values[i]`.

**Beklenen çıktı:**

```
3
-1
0
```
