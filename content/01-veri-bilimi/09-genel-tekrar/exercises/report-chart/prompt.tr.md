Gruplama ile görselleştirmeyi birleştireceksin: **hesapla, sırala, çiz,
kaydet.** Rapora giren grafik tam olarak böyle üretiliyor.

Veri `students.csv` dosyasında:

```text
name,city,age,hours,score
Ada,Ankara,21,12,82
Kerem,Izmir,23,6,74
Mina,Ankara,22,14,91
Deniz,Bursa,25,4,68
Efe,Ankara,21,11,88
Sila,Izmir,24,8,76
...
```

**Yapman gerekenler:**

1. İçe aktarmaları yaz ve dosyayı oku.
2. Şehre göre not ortalamasını hesapla, bir ondalığa yuvarla ve **büyükten
   küçüğe sırala**; sözlük olarak yazdır.
3. Ortalamaları çubuk grafik olarak çiz; ekseni **0 ile 100 arasına** aç.
4. Başlığı `Average score by city`, y eksenini `Score` yap.
5. **`report.png`** olarak kaydet (`dpi=150`, `bbox_inches="tight"`) ve
   tuvali kapat.
6. Tek satırda yan yana yazdır: çubuk sayısı, eksenin üst sınırı (tam
   sayı), başlık.

**Beklenen çıktı:**

```
{'Ankara': 85.2, 'Adana': 82.0, 'Izmir': 71.3, 'Bursa': 70.0}
4 100 Average score by city
```

Çalıştırdıktan sonra grafiğin **sonuç panelinde** görünecek.

**Bu, modülün en çok tekrarlanan kalıbı:**

```python
averages = data.groupby("city")["score"].mean()
ax.bar(averages.index, averages.values)
```

**Sıralamak bir tercih değil, okunurluk.** Çubuklar alfabetik dururken
okuyan kişi en yükseği gözüyle aramak zorunda; sıralı durunca ilk çubuk
cevap. **Ekseni sıfırdan başlatmak** da bir tercih değil: çubuğun uzunluğu
değeri temsil ediyor.
