Önceki alıştırmada üç eşik gördün. Şimdi **hepsini** görecek ve takası
grafiğe dökeceksin.

**Yapman gerekenler:**

1. Aynı akışı kur, modeli eğit, pozitif sınıfın olasılığını al.
2. **0.05'ten 0.95'e** kadar beşer beşer eşikler üret.
3. Her eşik için precision ve recall hesapla, ikisini ayrı listelerde
   birikt.
4. İki eğriyi aynı grafiğe çiz: yatayda eşik, dikeyde skor. Her eğriye
   `precision` ve `recall` etiketlerini ver ve **açıklama kutusunu**
   (`legend`) ekle.
5. Eksenleri `threshold` ve `score` diye adlandır, başlık koy, `chart.png`
   olarak kaydet.
6. Recall'ı **0.9'un altına düşürmeyen en yüksek eşiği** yazdır.

**Beklenen çıktı:**

```
0.65
```

Grafiğin çalıştırma sonrası **sonuç panelinde** görünecek.

**Grafikte göreceğin şey iki ters eğri:** precision soldan sağa yükseliyor,
recall düşüyor. Kesiştikleri yer, ikisinin dengede olduğu nokta.

**Yazdırdığın 0.65 bir karar.** "Recall en az %90 olsun" bir kısıt; o kısıt
altında precision'ı olabildiğince yükselten eşik bu. Gerçek projelerde
karar tam olarak böyle veriliyor: **bir tarafa alt sınır konup öteki en
iyilenir.**

O alt sınırı model kuran kişi tek başına uyduramıyor. "Geçecek öğrencilerin
en fazla %10'unu kaçırabiliriz" cümlesi işi yapan kişiden geliyor;
mühendislik kararı değil, alan kararı.

**Bir uyarı:** burada eşiği test kümesine bakarak seçtik. Gerçek bir
projede bu, testi eğitim verisine çevirirdi — eşik **doğrulama** kümesinde
seçilir, teste yalnızca sonda bir kez bakılır. 5. bölümün konusu.
