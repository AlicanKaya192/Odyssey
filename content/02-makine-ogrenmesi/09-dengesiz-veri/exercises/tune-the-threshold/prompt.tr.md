`predict()` aslında olasılığı **0,5** ile karşılaştırıyor. Bu sayı
sklearn'in seçtiği bir varsayılan, veriden gelen bir şey değil.

Dengesiz veride 0,5 neredeyse hiçbir zaman doğru yer değil: model
pozitiflere zaten düşük olasılık veriyor.

**Yapman gerekenler:**

1. Veriyi hazırla, ayır ve ölçekle. `LogisticRegression(max_iter=1000)`
   eğit.
2. `predict_proba` ile pozitif sınıfın olasılığını al.
3. Şu eşikleri sırayla dene: **0.5, 0.4, 0.3, 0.2, 0.1, 0.05**.
4. Her eşik için tek satır yazdır: **eşik, precision, recall, F1,
   yakalanan dolandırıcılık sayısı** (üç ondalık).
5. Son satırda **en yüksek F1'i veren eşiği** ve o F1 değerini yan yana
   yazdır.

**Beklenen çıktı:**

```
0.5 0.75 0.286 0.414 6
0.4 0.6 0.286 0.387 6
0.3 0.5 0.286 0.364 6
0.2 0.5 0.333 0.4 7
0.1 0.342 0.619 0.441 13
0.05 0.262 0.762 0.39 16
0.1 0.441
```

**Eşik 0,10'da F1 tepe yapıyor: 0,441.** Varsayılan 0,5'te 0,414 idi.

**Bu satırın önemi şurada:** model hiç değişmedi. Aynı katsayılar, aynı
olasılıklar, yeniden eğitim yok. Değişen tek şey **kararın verildiği
yer** — ve yakalanan dolandırıcılık sayısı 6'dan 13'e çıktı.

**0,05'e inince ne oluyor?** Recall 0,762'ye çıkıyor (16 yakalanıyor) ama
precision 0,262'ye düşüyor ve F1 geri geliyor. "Eşiği düşür, recall
artsın" sınırsız bir strateji değil.

**Bir uyarı:** burada eşiği **test kümesine bakarak** seçtin. Gerçek bir
projede bu bölüm 05'teki sızıntının aynısı olurdu — eşik doğrulama
kümesinde ya da çapraz doğrulamayla seçilir, test kümesi yalnızca son
raporu verir.

**İkinci uyarı:** F1 precision ile recall'ü eşit önemde sayıyor. İş
dünyası genelde saymıyor. Bir kaçırma 400 lira, bir yanlış alarm 5 lira
ise beklenen maliyet 0,05'i seçiyor, F1'in dediği 0,10'u değil.

**Eşik seçimi bir model kararı değil, bir iş kararı.**
