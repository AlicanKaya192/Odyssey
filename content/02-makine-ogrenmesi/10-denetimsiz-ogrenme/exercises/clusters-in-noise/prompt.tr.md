Üçüncü alıştırmada silüet 0.525 çıktı. **İyi mi?**

Bu soruya cevap veremezsin — neye göre iyi? Bu alıştırmada referansı
kuracaksın.

**Yöntem:** aynı boyutta, aynı sütun sayısında, **hiçbir yapısı olmayan**
rastgele bir veri üret ve aynı kümelemeyi ona da uygula.

**Yapman gerekenler:**

1. Veriyi hazırla ve ölçekle.
2. `numpy.random.default_rng(0)` ile `X_scaled` ile **aynı biçimde**
   standart normal bir gürültü dizisi üret.
3. `k` değerini **2'den 5'e** kadar dene. Her `k` için tek satır yazdır:
   **k, gerçek verinin silüeti, gürültünün silüeti** (üç ondalık).
4. Gürültüde `k=4` ile bulunan küme boyutlarını sıralı liste olarak
   yazdır.
5. Son satırda `k=4`'teki iki silüetin oranını yazdır (bir ondalık).

**Beklenen çıktı:**

```
2 0.514 0.169
3 0.525 0.176
4 0.517 0.181
5 0.489 0.185
[80, 82, 94, 94]
2.9
```

**Dördüncü satıra bak: gürültüde dört küme var.** Boyutları da makul
görünüyor — 80, 82, 94, 94. Ortada hiçbir grup yok, model yine de dört
tane döndürdü.

**Birinci ders: küme döndürmesi, küme olduğunun kanıtı değil.** Algoritma
ne verirsen bölüyor. "KMeans çalıştırdım, dört küme buldum" cümlesi
hiçbir şey söylemiyor.

**İkinci ders: gürültü sütununa dikkat.** 0.169 → 0.176 → 0.181 → 0.185:
`k` arttıkça silüet **artıyor**. Yani "silüeti maksimize eden `k`'yı seç"
bir yöntem değil; gürültüde bile bir tepe noktası veriyor.

**Son satır: 2.9.** Gerçek veri gürültünün yaklaşık **üç katı** silüet
veriyor. Asıl bilgi bu orandır, 0.517 sayısı değil.

İki değer birbirine yakın çıksaydı — mesela 0.22'ye karşı 0.18 — kümelerin
algoritmanın verdiği keyfi bölmeler olduğunu düşünmen gerekirdi.

**Ama sayı da tek başına yetmiyor.** Kümelerin gerçek olup olmadığının
asıl testi birinci alıştırmadaki tabloda: **her satıra bir isim
verebiliyor musun?** "Sık gelen, az alan grup" diyebiliyorsan küme bir şey
anlatıyor.
