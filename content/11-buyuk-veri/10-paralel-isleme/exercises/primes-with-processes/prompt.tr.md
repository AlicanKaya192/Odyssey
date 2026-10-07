0 ile 100 000 arasındaki asal sayıları dört parçaya bölüp bir süreç
havuzuyla say ve sonucu sıralı çözümle karşılaştır.

**Yapman gerekenler:**

1. `count_primes` fonksiyonu başlangıç kodunda hazır.
2. `if __name__ == "__main__":` bloğunun içinde:
   - `parts = [(i * 25_000, (i + 1) * 25_000) for i in range(4)]`,
   - `ProcessPoolExecutor(max_workers=2)` ile `ex.map(count_primes, parts)`
     sonucunu bir listeye al ve yazdır,
   - toplamı yazdır,
   - aynı toplamı sıralı olarak (`sum(map(count_primes, parts))`) hesapla ve
     iki toplamın eşit olup olmadığını yazdır.

**Beklenen çıktı:**

```
[2762, 2371, 2260, 2199]
9592
True
```
