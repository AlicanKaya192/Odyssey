`sum_digits(n)` fonksiyonunu **özyinelemeyle** yaz: negatif olmayan bir tam
sayının rakamlarının toplamını döndürsün. Döngü kullanma.

- `sum_digits(1234)` → `10`

**Üç soru:**

1. En küçük hâli: `n` tek basamaklıysa (`n < 10`) cevap `n`.
2. Bir adım küçültmek: son rakam `n % 10`, geri kalan `n // 10`.
3. Birleştirmek: son rakam + geri kalanın rakamlar toplamı.

**Beklenen çıktı:**

```
10
7
45
```
