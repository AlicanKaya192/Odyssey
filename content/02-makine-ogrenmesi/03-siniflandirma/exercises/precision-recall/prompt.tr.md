Karışıklık matrisindeki dört sayıyı iki anlamlı orana indireceksin — ve
ikisini de formülden kuracaksın.

**Yapman gerekenler:**

1. Aynı akışı kur ve karışıklık matrisinden dört sayıyı çıkar.
2. **Precision**'ı hesapla: `TP / (TP + FP)`. Üç ondalıkla yazdır.
3. **Recall**'ı hesapla: `TP / (TP + FN)`. Üç ondalıkla yazdır.
4. **F1**'i hesapla: `2 x precision x recall / (precision + recall)`.
   Üç ondalıkla yazdır.
5. sklearn'in verdiği üç değeri **tek satırda yan yana** yazdır (aynı sıra,
   üç ondalık).

**Beklenen çıktı:**

```
0.839
0.963
0.897
0.839 0.963 0.897
```

**İki oranın farkı paydalarında:**

- **Precision 0.839** — payda `TP + FP` = **senin tahminlerin**. "Geçti
  dediğim 31 kişinin 26'sı gerçekten geçti."
- **Recall 0.963** — payda `TP + FN` = **gerçekte var olanlar**. "Geçen 27
  kişinin 26'sını buldum."

Aynı `TP` sayısı, iki farklı payda, iki farklı soru.

**Recall precision'dan yüksek çıktı.** Model geniş bir ağ atıyor: geçenleri
neredeyse hiç kaçırmıyor ama bazı kalanları da içine alıyor. Karışıklık
matrisindeki 5 yanlış pozitif tam olarak bu.

**F1 neden harmonik ortalama?** Sıradan ortalama olsaydı, bir tek kişiye
"geçti" deyip tutturan bir model (precision 1.0, recall 0.037) 0.52 alırdı
ve idare eder görünürdü. Harmonik ortalama **0.071** veriyor: biri çok
düşükse sonuç da düşük.
