Bir sınavın notlarını özetleyeceksin ve **ortalamanın neden yanıltabildiğini**
grafikte göreceksin.

Veri `exam.csv` dosyasında; ilk satırları şöyle:

```text
student,score
S01,95
S02,92
S03,90
S04,88
S05,88
S06,86
...
```

**Yapman gerekenler:**

1. İçe aktarmaları yaz ve dosyayı oku.
2. `score` sütununun ortalamasını (iki ondalık), medyanını ve standart
   sapmasını (iki ondalık) sırayla yazdır.
3. Ortalama medyandan küçük mü? `True` ya da `False` yazdır.
4. Notların **histogramını** çiz (`bins=6`).
5. Ortalamayı **kırmızı kesik** dikey çizgiyle, medyanı **yeşil** dikey
   çizgiyle işaretle; ikisine de etiket ver ve lejant koy.
6. Başlığı `Exam scores`, x eksenini `Score` yap, **`histogram.png`**
   olarak kaydet.

**Beklenen çıktı:**

```
73.2
84.0
22.89
True
```

Çalıştırdıktan sonra grafiğin **sonuç panelinde** görünecek.

**Grafikte göreceğin şey:** notların çoğu 80–95 arasında toplanmış, solda
birkaç çok düşük not var. O dört düşük not **ortalamayı aşağı çekiyor**;
kırmızı çizgi, öğrencilerin çoğunun durduğu yerin epey solunda. Medyan ise
ortadaki öğrenciye bakıyor ve uç değerlerden etkilenmiyor — yeşil çizgi
kalabalığın içinde.

**Kural:** dağılım bir yana yatıksa "tipik değer" için medyana bak.
Ortalamayı raporlayacaksan medyanı da yanına yaz.
