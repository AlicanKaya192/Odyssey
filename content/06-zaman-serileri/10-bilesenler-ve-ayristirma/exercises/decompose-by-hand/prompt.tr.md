Günlük satışı kütüphane kullanmadan üç bileşene ayır.

**Yapman gerekenler:**

1. `trend`: 7 günlük ortalanmış hareketli ortalama.
2. `detrended = s - trend`. Haftanın gününe göre ortalamasını al
   (`groupby(detrended.index.dayofweek).mean()`) ve toplamı sıfır olsun diye
   kendi ortalamasını çıkar. Buna `pattern` de.
3. `pattern`'i bir ondalığa yuvarlayıp liste olarak yazdır (pazartesiden
   pazara yedi sayı).
4. Deseni bütün tarihlere yay:
   `seasonal = pd.Series(pattern.loc[s.index.dayofweek].values, index=s.index)`.
5. `resid = s - trend - seasonal`. Kalıntının ve serinin standart sapmasını
   iki ondalığa yuvarlayıp aynı satıra yazdır.
6. 12 Mart 2024 için gözlemi, trendi, mevsimi ve kalıntıyı (bir ondalık) aynı
   satıra yazdır.
7. Üç bileşenin toplamı seriyi geri veriyor mu? `NaN` olmayan günlerde
   `(trend + seasonal + resid - s).abs().max() < 1e-9` sonucunu yazdır.

**Beklenen çıktı:**

```
[-42.6, -39.6, -31.1, -18.7, 19.0, 76.2, 36.7]
12.32 58.94
256 287.9 -39.6 7.8
True
```

Cumartesi trendin 76 üstünde, pazartesi 43 altında. Standart sapma 58.94'ten
12.32'ye indi: satıştaki oynaklığın çoğu trend ve haftalık desenle
açıklanıyor.
