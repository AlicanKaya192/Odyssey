Bu alıştırma adı olan bir tuzağı gösteriyor: **Simpson paradoksu.**

Başlangıç kodundaki `records` tablosunda iki takımın çözdüğü sorular var:
takım, sorunun zorluğu ve alınan puan.

**Yapman gerekenler:**

1. Takım ortalamalarını hesapla ve **A ile B'yi yan yana** yazdır.
2. Ortalaması yüksek olan takımı yazdır.
3. Her takımın kaç **zor** soru çözdüğünü yan yana yazdır (A, sonra B).
4. **Kolay** sorulardaki ortalamaları yan yana yazdır (A, sonra B).
5. **Zor** sorulardaki ortalamaları yan yana yazdır (A, sonra B).

**Beklenen çıktı:**

```
74.0 61.0
A
2 8
80.0 85.0
50.0 55.0
```

**Şimdi çıktıyı oku.** Genel ortalamada A önde: 74'e karşı 61.

Ama son iki satıra bak: **kolay sorularda B daha iyi (85 > 80), zor
sorularda da B daha iyi (55 > 50).** Her iki seviyede de B kazanıyor, genel
ortalamada A kazanıyor.

Sebep üçüncü satırda: A yalnızca 2 zor soru çözmüş, B ise 8. B'nin ortalaması
zor soruların ağırlığı yüzünden düşük çıkıyor.

**Genel ortalama yalan söylemiyor, eksik soruya cevap veriyor.** Bir grup
farkı bulduğunda sorulacak soru şu: *bu grupların başka bir şeyi de farklı
mı?* Cevap evetse o sütuna göre de kırman gerekiyor.
