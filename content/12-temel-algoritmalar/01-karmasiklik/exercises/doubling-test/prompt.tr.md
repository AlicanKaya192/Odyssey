Bir algoritmanın sınıfını ölçerek bulmanın pratik yolu **iki kat testi**:
girdiyi iki katına çıkar, iş kaç katına çıkıyor bak.

1. `count_triples(n)` fonksiyonunu **iç içe üç döngüyle** yaz: `0`'dan
   `n-1`'e kadar sayılardan `i < j < k` olan her **üçlüyü** bir kez saysın.
2. `n` değeri 10, 20, 40 ve 80 için `n`'yi, üçlü sayısını ve bir önceki
   `n`'ye göre oranı (`yeni / eski`, `round(..., 2)` ile) yazdır. İlk satırda
   oran yok.

**Beklenen çıktı:**

```
10 120
20 1140 9.5
40 9880 8.67
80 82160 8.32
```

Oran 8'e yaklaşıyor: `2³ = 8`. Üç iç içe döngü `O(n³)`.
