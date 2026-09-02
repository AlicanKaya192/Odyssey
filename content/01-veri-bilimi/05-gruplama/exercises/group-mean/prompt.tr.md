İlk bölümde on satır yazarak yaptığın işi bir satırda yapacaksın.

**Yapman gerekenler:**

1. Her şehrin not ortalamasını hesapla, `averages` adlı seride tut.
2. `averages` serisini **iki basamağa yuvarlanmış** olarak yazdır.
3. Her şehirde kaç kişi olduğunu yazdır.
4. En yüksek ortalamaya sahip şehrin adını yazdır.

**Beklenen çıktı:**

```
city
Ankara    87.00
Bursa     69.00
Izmir     71.33
Name: score, dtype: float64
city
Ankara    3
Bursa     2
Izmir     3
dtype: int64
Ankara
```

**Dikkat edeceğin iki şey:**

- Gruplar **alfabetik** sıralanıyor — veride hangi sırada olduklarından
  bağımsız.
- Sonuç bir seri ve şehir adları **index**'te. Bu yüzden `idxmax()` sana
  doğrudan şehrin adını verebiliyor.
