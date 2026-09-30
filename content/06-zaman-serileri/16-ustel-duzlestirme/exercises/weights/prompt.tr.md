Üstel düzleştirmede `k` adım gerideki gözlemin ağırlığı `α × (1 − α) ** k`.
Bu ağırlıkların nasıl davrandığını sayılarla gör.

**Yapman gerekenler:**

1. `weights(alpha, n)` fonksiyonunu yaz: en yeni `n` gözlemin ağırlıklarını
   (k = 0, 1, ..., n − 1) liste olarak döndürsün.
2. `α = 0.3` için ilk 6 ağırlığı üç ondalığa yuvarlayıp liste olarak yazdır.
3. `α = 0.3` için ilk 10 ağırlığın toplamını üç ondalığa yuvarlayıp yazdır.
4. `α = 0.9` için ilk 3 ağırlığı üç ondalıkla liste olarak yazdır.
5. Ağırlıkların toplamının 0.95'i geçmesi için en yeni kaç gözlem gerekiyor?
   `α = 0.1`, `0.3` ve `0.9` için bu sayıyı bulup liste olarak yazdır.

**Beklenen çıktı:**

```
[0.3, 0.21, 0.147, 0.103, 0.072, 0.05]
0.972
[0.9, 0.09, 0.009]
[29, 9, 2]
```

`α = 0.9`'da ağırlığın %90'ı tek bir gözlemde: neredeyse naif tahmin.
`α = 0.1`'de ağırlığın %95'ine ulaşmak için 29 gözlem gerekiyor: tahmin
yaklaşık bir aylık geçmişin ortalaması gibi davranıyor. Tek bir sayı, modelin
ne kadar geriye baktığını belirliyor.
