# Dengesiz Veri

Bölüm 03'te doğruluğun tek başına yetmediğini gördün: %85 doğruluk, taban
çizgi %67,5 iken pek de parlak değildi. Ama orada sınıflar kabaca dengeliydi.

Bu bölümde sınıflardan biri **%5,7**. Ve orada doğruluk yalnızca yetersiz
kalmıyor — **aktif olarak yanıltıyor.**

Veri 1500 kart işlemi: `amount` (tutar), `hour` (saat), `attempts`
(o gün kaçıncı deneme) ve hedef `fraud` (dolandırıcılık mı). 1500 satırın
**85 tanesi** dolandırıcılık.

## Hiçbir şey yapmayan model

Taban çizgiyi kur: her şeye "dolandırıcılık değil" de.

```python
zeros = [0] * len(y_test)
print(accuracy_score(y_test, zeros))   # 0.944
```

**%94,4 doğruluk.** Bir satır bile model kodu yazmadan.

Bu sayıyı bir sunumda görsen etkilenirdin. Oysa model hiçbir dolandırıcılığı
yakalamıyor — tek bir tanesini bile. Ürün olarak değeri **sıfır**.

Şimdi gerçek modeli kur:

```python
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)
prediction = model.predict(X_test_scaled)

print(accuracy_score(y_test, prediction))   # 0.955
```

**%95,5.** Taban çizgiden 1,1 puan yukarıda. Model bir şey öğrendi mi?

## Karışıklık matrisi cevabı veriyor

```python
print(confusion_matrix(y_test, prediction))
# [[352   2]
#  [ 15   6]]
```

Test kümesinde 21 dolandırıcılık var. Model **6 tanesini** yakalamış,
**15 tanesini** kaçırmış.

```python
print(precision_score(y_test, prediction))   # 0.75
print(recall_score(y_test, prediction))      # 0.286
```

Precision 0,75 — "dolandırıcılık" dediklerinin dörtte üçü gerçekten öyle.
Recall **0,286** — gerçek dolandırıcılıkların yalnızca %28,6'sı yakalanmış.

**Doğruluk 0,955 ile 0,944 arasındaki fark neredeyse yok; recall 0 ile
0,286 arasındaki fark ise her şey.** İki modeli doğruluğa göre
karşılaştırmak, aralarındaki tek gerçek farkı görmemek demek.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Doğruluk: 0.944 → 0.955</h4>
      <p>1,1 puanlık artış. Grafiğe koysan düz çizgi gibi durur.</p>
    </div>
    <div class="versus-side">
      <h4>Recall: 0.000 → 0.286</h4>
      <p>Hiçbir şeyden altı yakalamaya. Ürün açısından tek anlamlı fark.</p>
    </div>
  </div>
  <figcaption>Aynı iki model, aynı test kümesi. Ölçüyü seçen kişi sonucu da seçiyor.</figcaption>
</figure>

## Neden böyle oluyor

Model kasten tembellik yapmıyor. Eğitim sırasında **toplam hatayı**
azaltmaya çalışıyor ve elindeki 1125 satırın 1068'i negatif.

Bir negatifi yanlış bilmek 1068 satırlık grubu bozuyor; bir pozitifi
kaçırmak 57 satırlık grubu. Matematik açısından temkinli davranmak
kârlı: **"emin değilsen negatif de"** stratejisi hatayı gerçekten
düşürüyor.

Sorun modelde değil, modele sorduğumuz soruda. Biz "toplam hatayı azalt"
dedik; oysa istediğimiz "dolandırıcılıkları yakala"ydı.

## Birinci çare: sınıfları ağırlıklandırmak

Modele "bir pozitifi kaçırmak, bir negatifi yanlış bilmekten daha pahalı"
demenin bir yolu var:

```python
model = LogisticRegression(max_iter=1000, class_weight="balanced")
```

`"balanced"`, her sınıfa **sıklığının tersi** oranında ağırlık veriyor.
Pozitifler on sekiz kat daha az olduğu için bir pozitif hatası on sekiz kat
ağır sayılıyor.

Ölçülen sonuç:

| | Doğruluk | Precision | Recall | F1 |
|---|---|---|---|---|
| Varsayılan | 0.955 | 0.750 | 0.286 | 0.414 |
| `balanced` | 0.880 | 0.269 | 0.667 | 0.384 |

**Recall 0,286'dan 0,667'ye çıktı** — 6 yerine 14 dolandırıcılık yakalanıyor.

**Bedeli açık:** precision 0,75'ten 0,269'a düştü. Model 52 işleme
"dolandırıcılık" diyor, 38'i yanlış alarm. Doğruluk da 0,955'ten 0,880'e
indi.

Bu bir **takas**, bir iyileştirme değil. Hangisinin doğru olduğu problemin
kendisine bağlı: kaçan bir dolandırıcılık mı daha pahalı, yoksa boşuna
bloke edilen bir müşteri mi?

`class_weight` ağaç tabanlı modellerde de var:

| | Doğruluk | Precision | Recall | F1 |
|---|---|---|---|---|
| Orman | 0.955 | 0.750 | 0.286 | 0.414 |
| Orman + `balanced` | 0.952 | 0.615 | 0.381 | 0.471 |

Ormanda etki daha ölçülü: recall 0,286'dan 0,381'e çıkıyor, precision
0,75'ten 0,615'e düşüyor. F1 ise yükseliyor — bu veride en dengeli sonuç.

## İkinci çare: eşiği oynatmak

Bölüm 03'te eşiği tanımıştın: `predict` aslında `predict_proba` çıktısını
0,5 ile karşılaştırıyor. Dengesiz veride 0,5 neredeyse hiçbir zaman doğru
yer değil.

```python
probability = model.predict_proba(X_test_scaled)[:, 1]
prediction = (probability >= 0.1).astype(int)
```

Ölçülen tarama:

| Eşik | Precision | Recall | F1 | Yakalanan / 21 |
|---|---|---|---|---|
| 0.50 | 0.750 | 0.286 | 0.414 | 6 |
| 0.30 | 0.500 | 0.286 | 0.364 | 6 |
| 0.20 | 0.500 | 0.333 | 0.400 | 7 |
| **0.10** | 0.342 | 0.619 | **0.441** | 13 |
| 0.05 | 0.262 | 0.762 | 0.390 | 16 |

**Eşik 0,10'da F1 tepe yapıyor:** 0,414'ten 0,441'e. Aynı model, aynı
katsayılar, yeniden eğitim yok — yalnızca kararın verildiği yer değişti.

0,05'e inince recall 0,762'ye çıkıyor ama precision 0,262'ye düşüyor ve F1
geri geliyor. Yani "eşiği düşür, recall artsın" sınırsız bir strateji değil.

**Eşik seçimi bir model kararı değil, bir iş kararı.** Yanlış alarmın
maliyetini bilen kişi bu tabloya bakıp seçmeli. Ama seçim **eğitim
tarafında** yapılmalı, test kümesine bakarak değil — bölüm 05'in kuralı
burada da geçerli.

## Eşiğe bağlı olmayan ölçüler

Precision, recall ve F1'in hepsi tek bir eşiğe bağlı. Peki modelin
**sıralama yeteneğini** ölçmenin bir yolu var mı? Yani riskli işlemleri
listenin üstüne koyabiliyor mu?

```python
from sklearn.metrics import roc_auc_score, average_precision_score

print(roc_auc_score(y_test, probability))          # 0.908
print(average_precision_score(y_test, probability)) # 0.525
```

**ROC AUC 0,908.** Rastgele seçilmiş bir dolandırıcılığa, rastgele seçilmiş
bir normal işlemden yüksek olasılık verme ihtimali %90,8. Kulağa harika
geliyor.

**Ortalama precision 0,525.** Aynı model, aynı olasılıklar. Neden bu kadar
düşük?

Çünkü **ROC eğrisi dengesiz veride iyimser.** Yanlış pozitif oranını 354
negatife bölüyor; 38 yanlış alarm bile oranı yalnızca 0,107 yapıyor.
Precision-recall eğrisi ise yanlış alarmları **pozitiflerle** karşılaştırıyor
ve orada 38 yanlış alarm, 14 doğru yakalamanın yanında çok görünüyor.

**Taban çizgisi de farklı:** rastgele bir modelin ROC AUC'si 0,5; ortalama
precision'ı ise **pozitif oranı**, yani burada 0,056. Yani 0,525 aslında
tabanın dokuz katı — kötü bir sayı değil, sadece 0,908 kadar iyimser değil.

| Model | ROC AUC | Ortalama precision |
|---|---|---|
| Lojistik regresyon | 0.908 | 0.525 |
| Rastgele orman | 0.834 | 0.426 |
| Rastgele tahmin | 0.500 | 0.056 |

**Kural:** dengesiz veride ROC AUC'yi tek başına raporlama. Ortalama
precision (PR eğrisinin altındaki alan) azınlık sınıfına çok daha duyarlı.

## Çapraz doğrulamada hangi ölçü

`cross_val_score` varsayılan olarak doğruluk hesaplıyor. Dengesiz veride
bu, beş katı da aynı sayıyı vermeye yakın:

```python
cross_val_score(model, X_train_scaled, y_train, cv=skf, scoring="recall")
```

Ölçülen sonuç:

| `scoring` | Ortalama | Yayılım |
|---|---|---|
| `accuracy` | 0.952 | 0.008 |
| `recall` | 0.317 | 0.188 |
| `f1` | 0.397 | 0.183 |
| `roc_auc` | 0.930 | 0.028 |
| `average_precision` | 0.521 | 0.144 |

**Doğruluğun yayılımı 0,008.** Ne yaparsan yap bu sayı kıpırdamıyor; bir
hiperparametre taramasında hangi ayarın iyi olduğunu asla söyleyemez.

**Recall'ün yayılımı 0,188** — yirmi kat fazla. Çünkü her katta yalnızca
~17 pozitif var ve birkaçının kaçması sayıyı belirgin oynatıyor. Bu
**gürültü**, ama en azından gerçek bir sinyali de taşıyor.

`roc_auc` ve `average_precision` ikisi arasında duruyor: azınlık sınıfına
duyarlılar ama tek tek kayıtlara bağlı olmadıkları için daha kararlılar.
Dengesiz veride hiperparametre araması genelde bu ikisiyle yapılıyor.

## Yeniden örnekleme: yapmadığımız şey

Dengesizlikle başa çıkmanın üçüncü bir yolu daha var: **veriyi
değiştirmek.**

- **Aşağı örnekleme:** çoğunluk sınıfından rastgele satır atmak. Hızlı,
  ama gerçek veriyi çöpe atıyorsun.
- **Yukarı örnekleme:** azınlık sınıfını çoğaltmak. Hiçbir yeni bilgi
  eklemiyor, aynı satırları tekrarlıyor ve model onları ezberleyebiliyor.
- **SMOTE:** azınlık sınıfının komşuları arasında **yapay** satır üretmek.
  sklearn'de yok, `imbalanced-learn` paketinde.

Bu bölümde ikisini de kullanmadık, çünkü:

1. `class_weight` çoğu durumda aynı işi **veriyi bozmadan** yapıyor.
2. Yeniden örnekleme **yalnızca eğitim kümesine** uygulanabiliyor.
   Doğrulama veya test kümesini örneklemek sızıntının bir başka türü:
   gerçek dünyada dolandırıcılık oranı %5,7 ve model onu görmeli.
3. Çapraz doğrulamayla birleştirmek dikkat istiyor — örnekleme her katın
   **içinde** yapılmalı, öncesinde değil. Aynı sızıntı tuzağı.

Bilmen gereken şey adları ve bu üç uyarı; kütüphanesi gerektiğinde
öğrenilir.

## Karar sırası

<figure class="fig">
  <div class="flow">
    <span class="node"><b>1</b><br>taban çizgiyi<br>ölç</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>2</b><br>karışıklık matrisi<br>ve recall</span>
    <span class="arrow">&rarr;</span>
    <span class="node acc"><b>3</b><br>hangi hata<br>pahalı</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>4</b><br>ağırlık ve eşik<br>eğitimde</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>5</b><br>testte rapor:<br>ort. precision</span>
  </div>
  <figcaption>Üçüncü adım kod değil; iş kararı. Onu atlayan her ayar rastgele.</figcaption>
</figure>

## Bu bölümde neyi atladık

- **Çok sınıflı dengesizlik.** Buradaki her şey iki sınıf içindi. Üç ve
  daha fazlasında her sınıf için ayrı ölçüler hesaplanıp `macro` ya da
  `weighted` ortalamayla birleştiriliyor.
- **Maliyet matrisi.** Yanlış alarmın ve kaçırmanın parasal karşılığı
  biliniyorsa eşik F1'e değil, doğrudan **beklenen maliyete** göre
  seçilebiliyor. Formül basit; zor olan maliyetleri öğrenmek.
- **Anomali tespiti.** Pozitif sınıf %0,1 gibi uç bir seviyedeyse
  sınıflandırma yerine "normalden sapma" arayan modeller kullanılıyor
  (`IsolationForest` gibi).

Bu bölümün tek cümlelik özeti: **dengesiz veride ölçüyü seçmek, modeli
seçmekten daha önemli.**
