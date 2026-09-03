İkinci alıştırmada pipeline'ın sızıntıyı engellediğini söyledik. Şimdi
**ne kadar** engellediğini ölçeceksin.

Ölçekleme ve doldurma için etki genelde küçük. Ama **hedefe bakan** bir
adım varsa büyüyor. Özellik seçimi tam olarak öyle bir adım.

**Yapman gerekenler:**

1. Veriyi hazırla, ayır ve ön işlemeden geçir (dokuz sütun).
2. `numpy.random.default_rng(7)` ile **200 sütunluk tamamen rastgele**
   gürültü üret ve dokuz sütunun yanına ekle. Toplam sütun sayısını
   yazdır.
3. **Yanlış yol:** `SelectKBest(f_classif, k=15)` ile bütün eğitim
   verisinde en iyi 15 sütunu seç, sonra o 15 sütunda `cross_val_score`
   çalıştır.
4. **Doğru yol:** seçiciyi ve modeli bir `Pipeline`'a koyup 209 sütunun
   tamamıyla `cross_val_score` çalıştır.
5. İki CV ortalamasını ve aradaki farkı yazdır (üç ondalık).
6. Yanlış yolda seçilen 15 sütunun **kaç tanesinin gürültü** olduğunu
   yazdır (ilk dokuz sütun gerçek, gerisi gürültü).

**Beklenen çıktı:**

```
209
0.78
0.716
0.064
8
```

**6,4 puanlık fark, tamamen uydurma.**

Ne oldu: seçici **bütün eğitim verisine** baktı ve "şu 15 sütun hedefe en
çok benziyor" dedi. 209 sütun arasından 15 seçerken, tesadüfen hedefe
benzeyen gürültü sütunları bulmak kolay. Sonra aynı veride doğrulanınca
o sütunlar iyi görünüyor — çünkü seçim zaten o veriye göre yapılmıştı.

**Son satır bunu kanıtlıyor: seçilen 15 sütunun 8'i saf gürültü.** İçinde
hiçbir bilgi yok; yalnızca 450 satırlık bu örneklemde `churn` sütununa
benziyorlar.

**Doğru yolda seçim her katın içinde yapılıyor.** Birinci katta seçilen
gürültü sütunları, o katın doğrulama kısmında işe yaramıyor — çünkü orada
başka satırlar var. Numara bozuluyor ve gerçek skor ortaya çıkıyor:
0.716.

**Genel kural:** hedefe bakan her adım pipeline'ın içinde olmalı. Özellik
seçimi, hedef kodlaması, aykırı değer atma — hepsi.

**Bir uyarı:** doğru yoldaki 0.716, ikinci alıştırmadaki 0.738'den de
düşük. Sebebi basit — 200 gürültü sütunu modeli gerçekten zorluyor.
Gürültü eklemek zarar veriyor; asıl mesele, **yanlış ölçüm bu zararı
görünmez yapıyor.**
