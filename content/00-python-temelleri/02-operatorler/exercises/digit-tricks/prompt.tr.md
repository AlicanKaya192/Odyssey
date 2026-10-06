Elinde dört basamaklı bir sayı var:

```python
n = 4827
```

İki şey hesapla:

- `digit_sum`: basamaklarının toplamı (`4 + 8 + 2 + 7`)
- `reversed_number`: basamakları ters sırada olan sayı, **sayı olarak**
  (`7284`)

```
Sum of digits: 21
Reversed: 7284
```

Kural: Sayıyı metne çevirmek yok (`str()` kullanmak yasak). Yalnızca
aritmetik: `//` ve `%`.

İşe yarayan iki gözlem:

- `n % 10` sayının **son** basamağını verir (`4827 % 10` → `7`).
- `n // 10` son basamağı **atar** (`4827 // 10` → `482`).

İkisini birleştirerek her basamağı tek tek çıkarabilirsin. Ters sayıyı
kurarken her basamağın hangi basamak değerine (binler, yüzler…) gideceğini
düşün.

> Dikkat: `reversed_number` ekranda `7284` görünse de metin olmamalı;
> kontrol tipine de bakıyor.
