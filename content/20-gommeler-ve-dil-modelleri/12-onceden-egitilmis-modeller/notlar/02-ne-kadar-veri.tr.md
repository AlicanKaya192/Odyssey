Ön eğitim için ne kadar etiketsiz metin gerekir? Vektörleri 200, 1000,
5000 ve 20 000 talepten öğrenip 20 ve 50 etiketle deneyelim:

```python
for size in [200, 1000, 5000, 20000]:
    index, E = pretrain(unlabelled[:size])
    D = np.array([embed(t) for t in texts])
    print(size, len(index), curve_point(20)[1], curve_point(50)[1])
```

```text
200 171 0.735 0.841
1000 204 0.725 0.842
5000 323 0.728 0.857
20000 440 0.748 0.866
```

Sütunlar: etiketsiz talep sayısı, sözlük, 20 ve 50 etiketle doğruluk.

- 200 talep bile 50 etiketle %84,1 veriyor; 20 000 talep %86,6. Sözlük 171
  kelimeden 440'a büyüyor: az geçen kelimeler (yazım hataları, şehir adları)
  ancak çok metinde en az 3 kez görülüp sözlüğe giriyor.
- Kazanç bu küçük dünyada az, çünkü taleplerin dili dar ve kurallı: birkaç
  yüz talep kelimelerin çoğunu gösteriyor. Gerçek bir dilde yüz binlerce
  kelime ve sayısız kalıp var; nadir bir kelimenin iyi bir vektörü için
  milyonlarca cümle gerekir.
- Büyük dil modellerinin milyarlarca kelimeyle eğitilmesinin sebebi bu:
  dilin uzun kuyruğunu (nadir kelimeler, nadir yapılar) görmek. Bir önceki
  not ise miktarın tek başına yetmediğini gösterdi: metin doğru alandan
  gelmeli.
