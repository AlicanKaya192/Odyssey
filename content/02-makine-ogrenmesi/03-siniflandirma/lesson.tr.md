# Sınıflandırma

Şimdiye kadar hep bir **sayı** tahmin ettik: fiyat. Bu bölümde hedef bir
**kategori**: geçti mi kaldı mı, spam mı değil mi, hasta mı sağlıklı mı.

Akış değişmiyor — oku, ayır, taban çizgi kur, eğit, ölç. Değişen iki şey
var: kullanılan model ve **ölçüler**. İkincisi, ilkinden çok daha önemli.

## Kalıntı diye bir şey yok

Regresyonda hatayı `gerçek - tahmin` diye hesaplıyorduk. Sınıflandırmada
bu işlem tanımsız: "kedi" ile "köpek" arasındaki fark bir sayı değil.

Sınıflar `0` ve `1` diye kodlanmış olsa bile aradaki mesafe uydurma.
Üç sınıf varsa (`0`, `1`, `2`) durumu daha da açık: 2 ile 0 arasındaki
fark, 1 ile 0 arasındakinin iki katı değil — sadece farklı iki kategori.

Bu yüzden MAE, RMSE, R² burada işe yaramıyor. Yeni bir ölçü ailesi
gerekiyor.

## İlk sınıflandırıcı

Model **lojistik regresyon**. Adında "regresyon" geçiyor ama yaptığı iş
sınıflandırma — kafa karıştırıcı bir isim, sebebi tarihsel.

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
prediction = model.predict(X_test)
```

Üç adım aynı. `max_iter` bir hiperparametre: model çözümü aramak için
döngü kuruyor ve varsayılan 100 tur bazı verilerde yetmiyor, uyarı
veriyor.

## Doğruluk ve taban çizgi tuzağı

İlk akla gelen ölçü **doğruluk** (accuracy): doğru bilinen kayıtların
oranı.

```python
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, prediction))   # 0.85
```

%85. İyi mi?

Aynı soru, aynı cevap: **taban çizgiye bak.** Sınıflandırmada taban çizgi,
her şeye **en sık görülen sınıfı** demek.

```python
most_common = y_train.mode()[0]
baseline = accuracy_score(y_test, [most_common] * len(y_test))
print(baseline)   # 0.675
```

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Taban çizgi</h4>
      <p>Herkese "geçti" diyor.<br>Doğruluk <b>%67.5</b></p>
    </div>
    <div class="versus-side">
      <h4>Model</h4>
      <p>Üç sütuna bakıp karar veriyor.<br>Doğruluk <b>%85</b></p>
    </div>
  </div>
  <figcaption>Hiçbir şey öğrenmeyen bir satır %67.5 doğru. Modelin %85'i ancak bunun yanında anlam kazanıyor.</figcaption>
</figure>

**Buradaki tehlike:** verideki iki sınıf eşit olmadığı sürece taban çizgi
her zaman %50'nin üstünde çıkıyor. Sınıflardan biri %95 ise, hiçbir şey
öğrenmeyen bir satır **%95 doğru** oluyor ve "modelim %94 doğru" cümlesi
bir başarısızlığı anlatıyor.

Doğruluğun en büyük sorunu bu ve **9. bölümün tamamı buna ayrılmış**.

## Doğruluğun içini açmak

%85 doğru — peki **hangi** %85? Hatalar nerede?

```python
from sklearn.metrics import confusion_matrix
print(confusion_matrix(y_test, prediction))
# [[ 8  5]
#  [ 1 26]]
```

Bu dört sayıya **karışıklık matrisi** deniyor.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">TN = 8</span><span class="anat-body">gerçek 0, tahmin 0 — kalacak olana doğru şekilde "kaldı" dedi</span></div>
    <div class="anat-row"><span class="anat-label">FP = 5</span><span class="anat-body">gerçek 0, tahmin 1 — <b>kalacak olana "geçti" dedi</b></span></div>
    <div class="anat-row"><span class="anat-label">FN = 1</span><span class="anat-body">gerçek 1, tahmin 0 — <b>geçecek olana "kaldı" dedi</b></span></div>
    <div class="anat-row"><span class="anat-label">TP = 26</span><span class="anat-body">gerçek 1, tahmin 1 — geçecek olana doğru şekilde "geçti" dedi</span></div>
  </div>
  <figcaption>sklearn matrisi bu sırayla veriyor: satırlar gerçek, sütunlar tahmin. Sol üst köşe her zaman TN.</figcaption>
</figure>

Doğruluk bu dördünden hesaplanıyor: `(TN + TP) / toplam` = `34/40` = 0.85.

**Ama dört sayı, tek sayıdan çok daha fazlasını anlatıyor.** Burada
5 yanlış pozitife karşılık yalnızca 1 yanlış negatif var. Model
"geçti" demeye eğilimli.

Bu iyi mi kötü mü? Duruma göre:

- Bir **burs** kararıysa, hak etmeyene burs vermek (FP) pahalı.
- Bir **destek dersi** kararıysa, ihtiyacı olanı kaçırmak (FN) pahalı.

Aynı model, aynı sayılar — farklı sonuç.

## Precision ve recall

Karışıklık matrisi dört sayı; bunları iki anlamlı orana indiriyoruz.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Precision</h4>
      <p><code>TP / (TP + FP)</code></p>
      <p>"Geçti dediklerimin kaçı gerçekten geçti?"<br><b>26/31 = 0.839</b></p>
    </div>
    <div class="versus-side">
      <h4>Recall</h4>
      <p><code>TP / (TP + FN)</code></p>
      <p>"Geçenlerin kaçını bulabildim?"<br><b>26/27 = 0.963</b></p>
    </div>
  </div>
  <figcaption>Precision tahminlerinin ne kadar temiz, recall taramanın ne kadar geniş olduğunu ölçüyor.</figcaption>
</figure>

Ayrımı akılda tutmanın yolu, **paydaya bakmak**:

- Precision'ın paydası **senin tahminlerin** — ne kadar güvenilir konuştun.
- Recall'ın paydası **gerçekte var olanlar** — kaçını yakaladın.

**Hangisi önemli, probleme bağlı:**

| Problem | Öncelik | Neden |
|---|---|---|
| Hastalık taraması | **Recall** | Hastayı kaçırmak, fazladan tetkikten pahalı |
| Spam filtresi | **Precision** | Gerçek e-postayı spam'e atmak, bir spam'i geçirmekten kötü |
| Dolandırıcılık tespiti | **Recall** | Kaçan işlem para kaybı |
| Öneri sistemi | **Precision** | Kötü öneri kullanıcıyı kaybettiriyor |

## F1: ikisini tek sayıya indirmek

İki sayı yerine bir sayı isteniyorsa **F1** kullanılıyor:

```
F1 = 2 x (precision x recall) / (precision + recall)
```

Bu bir **harmonik ortalama** ve sıradan ortalamadan farkı önemli: biri
çok düşükse F1 de düşük çıkıyor.

Precision 1.0, recall 0.02 olan bir model düşün — bir tek kişiye "hasta"
diyor ve tutturuyor. Sıradan ortalama 0.51 verirdi, kabul edilebilir
görünürdü. F1 **0.039** veriyor.

**F1 bir kolaylık, bir çözüm değil.** Precision ve recall'ı ayrı ayrı
görmek her zaman daha bilgilendirici; F1 yalnızca modelleri sıralamak
gerektiğinde işe yarıyor.

## Eşik: modelin gizli ayarı

`predict` sana `0` ya da `1` veriyor. Ama modelin içinde bir **olasılık**
var:

```python
probability = model.predict_proba(X_test)[:, 1]
```

`predict`, bu olasılık **0.5'ten büyükse 1** diyor. 0.5 bir hesap sonucu
değil, bir **varsayılan** — ve değiştirilebiliyor.

```python
prediction = (probability >= 0.3).astype(int)
```

Eşiği oynatınca ne oluyor:

```
esik   precision   recall
0.30     0.818      1.000
0.50     0.839      0.963
0.70     0.889      0.889
```

<figure class="fig">
  <div class="flow">
    <span class="node"><b>Eşik ↓</b><br>daha çok "1" diyor</span>
    <span class="arrow">→</span>
    <span class="node ok"><b>Recall ↑</b><br>daha azını kaçırıyor</span>
    <span class="arrow">+</span>
    <span class="node acc"><b>Precision ↓</b><br>daha çok yanlış alarm</span>
  </div>
  <figcaption>Eşiği düşürmek bir takas: kaçırmayı azaltıyor, yanlış alarmı artırıyor. Bedava iyileşme yok.</figcaption>
</figure>

Eşiği 0.30'a çekince recall **1.000** — hiçbir geçeni kaçırmıyor. Bedeli
precision'ın düşmesi.

**Bu, modeli yeniden eğitmeden yapılan bir ayar.** Aynı model, aynı
katsayılar; yalnızca kararın verildiği nokta değişiyor. Bir hastalık
taramasında eşiği düşürmek genelde doğru karar; bir spam filtresinde
yükseltmek.

## Hepsi tek çağrıda

```python
from sklearn.metrics import classification_report
print(classification_report(y_test, prediction))
```

```
              precision    recall  f1-score   support

           0       0.89      0.62      0.73        13
           1       0.84      0.96      0.90        27

    accuracy                           0.85        40
```

**Her sınıf için ayrı satır var** ve bu önemli: modelin `1` sınıfında
recall'ı 0.96 iken `0` sınıfında 0.62. Yani kalacakları bulmakta çok daha
kötü — tek bir doğruluk sayısı bunu tamamen gizliyordu.

`support` her sınıfta kaç kayıt olduğunu söylüyor: 13'e 27. Dengesizlik
buradan okunuyor.

## Bu bölümde neyi atladık

- **ROC eğrisi ve AUC.** Bütün eşikleri birden değerlendiren bir ölçü.
  Eşik takasını tek sayıya indiriyor; dengesiz veri bölümünde geliyor.
- **Çok sınıflı problemler.** Buradaki her şey iki sınıf içindi. Üç ve
  daha fazlasında precision/recall her sınıf için ayrı hesaplanıp
  ortalanıyor — `macro` ve `weighted` ortalamalar oradan çıkıyor.
- **Ciddi dengesizlik.** Sınıflardan biri %95 ise bu bölümdeki ölçüler
  bile yanıltabiliyor. 9. bölümün konusu.

Şimdilik elinde iki şey var: hedefin kategori olduğu problemlerde model
kurabiliyorsun, ve tek bir doğruluk sayısına güvenmemeyi biliyorsun.
İkincisi daha değerli.
