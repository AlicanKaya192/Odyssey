Precision, recall ve F1'in hepsi tek bir eşiğe bağlı. Modelin
**sıralama yeteneğini** ölçmenin — riskli işlemleri listenin üstüne
koyabiliyor mu — iki yolu var.

**Yapman gerekenler:**

1. Veriyi hazırla, ayır, ölçekle. Lojistik regresyonu ve
   `RandomForestClassifier(n_estimators=200, random_state=42)` ormanını
   eğit (orman ölçeksiz veriyle).
2. Her ikisi için tek satır yazdır: **ad, ROC AUC, ortalama precision**
   (üç ondalık).
3. Ortalama precision'ın **taban çizgisini** yazdır — rastgele bir modelin
   alacağı değer, yani pozitif oranı (üç ondalık).
4. Lojistik regresyonun iki eğrisini **yan yana** çiz:
   - Solda ROC eğrisi (`roc_curve`), eksenler `fpr` ve `tpr`, başlık `ROC`.
   - Sağda precision-recall eğrisi, eksenler `recall` ve `precision`,
     başlık `PR`.
   - `chart.png` olarak kaydet.
5. Son satırda ROC AUC ile ortalama precision arasındaki farkı yazdır
   (lojistik regresyon, üç ondalık).

**Beklenen çıktı:**

```
logreg 0.908 0.525
forest 0.834 0.426
0.056
0.383
```

**ROC AUC 0,908.** Rastgele seçilmiş bir dolandırıcılığa, rastgele
seçilmiş bir normal işlemden yüksek olasılık verme ihtimali %90,8.
Kulağa harika geliyor.

**Ortalama precision 0,525.** Aynı model, aynı olasılıklar. Aradaki fark
**0,383** — son satırdaki sayı.

**Neden bu kadar açık?** ROC eğrisi yanlış pozitif oranını 354 negatife
bölüyor; 38 yanlış alarm bile oranı yalnızca 0,107 yapıyor. Precision-recall
eğrisi ise yanlış alarmları **pozitiflerle** karşılaştırıyor ve orada 38
yanlış alarm, 14 doğru yakalamanın yanında çok görünüyor.

**Taban çizgileri de farklı.** Rastgele bir modelin ROC AUC'si 0,5;
ortalama precision'ı ise pozitif oranı — burada **0,056**. Yani 0,525
aslında tabanın dokuz katı. Kötü bir sayı değil, sadece 0,908 kadar iyimser
değil.

**Kural:** dengesiz veride ROC AUC'yi tek başına raporlama. İki sayı
birlikte verilir; ikinci sayı azınlık sınıfı hakkında çok daha dürüst.

Grafikte de görünüyor: ROC eğrisi sol üst köşeye yapışıyor, PR eğrisi ise
recall arttıkça hızla düşüyor.
