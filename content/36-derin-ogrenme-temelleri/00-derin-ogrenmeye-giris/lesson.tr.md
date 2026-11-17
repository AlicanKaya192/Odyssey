# Derin Öğrenmeye Giriş

Makine öğrenmesi patikasında modellerin çoğu, bizim hazırladığımız
özelliklerle çalışıyordu: yaş, gelir, kelime sayısı. **Derin öğrenme**
(deep learning) bu hazırlığın büyük kısmını modele bırakır. Model üst üste
dizilmiş **katmanlardan** (layer) oluşur; her katman bir öncekinin
çıktısından biraz daha işe yarar bir temsil öğrenir. Ham pikselden "bu bir
7" kararına, ham sesten kelimeye böyle gidilir.

Bu modülde derin öğrenmenin temellerini **PyTorch** kütüphanesiyle
öğreneceğiz. ML Algoritmaları modülündeki Sinir Ağı bölümünde bir sinir
ağını NumPy ile sıfırdan kurmuştuk: ileri hesap, türevleri elle çıkaran
geri yayılım (backpropagation) ve ağırlıkları güncelleme. PyTorch aynı
fikri taşır, ama türevleri **kendisi** hesaplar ve hazır katmanlar verir.
O bölümü okumadıysan sorun değil; burada her parçayı baştan anlatacağız.

## Önce sonucu görelim

Ayrıntıya girmeden önce bir derin öğrenme modelinin baştan sona nasıl
eğitildiğine bakalım. Veri, scikit-learn'ün içinde gelen el yazısı
rakamlar: her biri 8×8 piksellik 1797 görüntü (internet gerekmiyor).
Görev, görüntüdeki rakamı (0–9) bulmak.

```python
import torch
from torch import nn
from sklearn.datasets import load_digits

torch.manual_seed(0)
digits = load_digits()
X = torch.tensor(digits.data, dtype=torch.float32) / 16
y = torch.tensor(digits.target)

model = nn.Sequential(nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, 10))
optimizer = torch.optim.SGD(model.parameters(), lr=0.5)
loss_fn = nn.CrossEntropyLoss()

for epoch in range(200):
    optimizer.zero_grad()
    loss = loss_fn(model(X[:1200]), y[:1200])
    loss.backward()
    optimizer.step()
    if epoch % 40 == 0:
        print(epoch, round(loss.item(), 2))

correct = (model(X[1200:]).argmax(dim=1) == y[1200:]).sum().item()
print(correct, "/", len(y) - 1200, round(correct / (len(y) - 1200), 2))
```

```text
0 2.33
40 0.48
80 0.2
120 0.13
160 0.1
544 / 597 0.91
```

- İlk 1200 görüntüyle eğittik, modelin hiç görmediği son 597 görüntüyle
  sınadık.
- **Kayıp** (loss) modelin ne kadar yanıldığının ölçüsü. Eğitim başında
  2,33, sonunda çok daha küçük: model öğreniyor.
- Görmediği 597 rakamın 544 tanesini doğru buldu.
- Asıl eğitim yalnızca dört satır: `zero_grad`, kayıp, `backward`, `step`.
  Bu modülün geri kalanı bu dört satırın her birini açıyor.

Eğitimin süresi bu bilgisayarda bir saniyenin altında. Kodu ve sayıları
modül boyunca tek tek açacağız; şimdilik yalnızca resmin tamamını görelim.

## Veri: görüntüden sayılara

Bir rakam görüntüsü modele 64 sayı olarak gidiyor: 8 satır × 8 sütun
piksel, her biri 0 (beyaz) ile 16 (koyu) arasında. İlk görüntüyü
karakterlerle çizelim:

```python
print(digits.data.shape, digits.target[:10].tolist())
for row in digits.images[0]:
    print("".join("#" if v > 6 else "." for v in row))
```

```text
(1797, 64) [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
...##...
..####..
..#..##.
..#..##.
..#..##.
..#..##.
..#.##..
...##...
```

Bu bir 0. Kodda `X = ... / 16` piksel değerlerini 0–1 aralığına
getiriyor; ağlar küçük ve benzer ölçekteki sayılarla daha rahat öğrenir.
`torch.tensor` NumPy dizisini PyTorch'un dizisine, **tensöre** (tensor)
çeviriyor. Tensörleri bir sonraki bölümde ayrıntılı göreceğiz.

## Model: katmanlar

`nn.Sequential` katmanları sırayla birbirine bağlıyor:

<figure class="fig">
  <div class="flow">
    <span class="node">64 piksel</span><span class="arrow">→</span>
    <span class="node">Linear<br><small>64 → 32</small></span><span class="arrow">→</span>
    <span class="node">ReLU</span><span class="arrow">→</span>
    <span class="node">Linear<br><small>32 → 10</small></span><span class="arrow">→</span>
    <span class="node acc">10 puan</span>
  </div>
  <figcaption>Modelin yolu: 64 sayı girer, her rakam için bir puan çıkar. En yüksek puanlı rakam tahmindir.</figcaption>
</figure>

- `nn.Linear(64, 32)`: 64 girdiden 32 çıktı hesaplayan katman. Her çıktı,
  girdilerin ağırlıklı toplamı artı bir sabit. Ağırlıklar ve sabitler
  modelin **parametreleri**; eğitim onları ayarlıyor.
- `nn.ReLU()`: negatif sayıları 0 yapan basit bir fonksiyon. Katmanlar
  arasına böyle doğrusal olmayan bir adım koymasak, üst üste iki doğrusal
  katman tek bir doğrusal katmandan farksız olurdu.
- Son katman 10 puan veriyor; `argmax` en yüksek puanın sırasını, yani
  tahmin edilen rakamı seçiyor.

Eğitilmiş modele birkaç test görüntüsü verelim:

```python
with torch.no_grad():
    scores = model(X[1200:1208])
print(scores.shape)
print(scores.argmax(dim=1).tolist())
print(y[1200:1208].tolist())
```

```text
torch.Size([8, 10])
[7, 7, 7, 5, 1, 0, 0, 2]
[7, 7, 3, 5, 1, 0, 0, 2]
```

Sekiz görüntü için 10'ar puan, yani `8 × 10`. Tahminler (ikinci satır)
gerçek etiketlerle (üçüncü satır) 7 görüntüde aynı.
`torch.no_grad()` "burada türev hesaplama" demek; yalnızca tahmin
yaparken gereksiz işi ve belleği önlüyor.

## Eğitim döngüsü: dört adım

Döngünün her turu (epoch) aynı dört adımı yapıyor:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>optimizer.zero_grad()</code></span><span>Önceki turdan kalan türevleri sıfırla.</span></div>
    <div class="anat-row"><span><code>loss = loss_fn(model(X), y)</code></span><span>İleri hesap: tahmin et ve yanılmayı ölç.</span></div>
    <div class="anat-row"><span><code>loss.backward()</code></span><span>Geri yayılım: her parametrenin kaybı nasıl etkilediğini (türevi) hesapla.</span></div>
    <div class="anat-row"><span><code>optimizer.step()</code></span><span>Her parametreyi kaybı azaltacak yöne biraz kaydır.</span></div>
  </div>
  <figcaption>Bir eğitim turunun dört adımı. Bu dört satır modülün her yerinde, hep bu sırayla.</figcaption>
</figure>

- `loss_fn = nn.CrossEntropyLoss()` sınıflandırma kaybı: doğru rakama
  düşük puan veren modeli çok cezalandırıyor.
- `torch.optim.SGD(..., lr=0.5)` **gradyan inişi** (gradient descent).
  `lr` öğrenme oranı (learning rate): her adımda ne kadar kaydırılacağı.
- `backward` türevleri kendisi hesaplıyor; NumPy'deki gibi elle türev
  yazmadık. PyTorch'un en büyük kolaylığı bu: **otomatik türev**
  (autograd).

## Derin öğrenme her zaman mı?

Aynı veriye makine öğrenmesi patikasındaki lojistik regresyonu verelim:

```python
from sklearn.linear_model import LogisticRegression

clf = LogisticRegression(max_iter=2000).fit(digits.data[:1200], digits.target[:1200])
print((clf.predict(digits.data[1200:]) == digits.target[1200:]).sum())
```

```text
547
```

Lojistik regresyon 547 görüntüyü doğru buldu; küçük ağımız
544. Basit model biraz daha iyi bile: 64 sayılık küçük,
düzgün bir veri setinde derin öğrenmenin üstünlüğü yok. Derin öğrenme
asıl farkını şu durumlarda gösterir:

- Veri **ham** ve büyük: yüksek çözünürlüklü fotoğraf, ses, uzun metin.
  Elle iyi özellik yazmak zor, katmanlar özellikleri kendisi öğreniyor.
- Çok veri var: binlerce, milyonlarca örnek. Büyük ağlar verisi çoğaldıkça
  iyileşmeye devam ediyor.
- Tablo verisinde (satır ve sütun) ise çoğu zaman ağaç tabanlı modeller
  (gradyan artırma) hâlâ çok güçlü; derin öğrenmeye geçmeden önce onları
  denemek iyi bir alışkanlık.

## Bu modülün yolu

- **Tensörler** ve tensör işlemleri: PyTorch'un dizisi.
- **Otomatik türev**: `backward` ne yapıyor; ilk modeli elle eğitmek.
- **nn.Module**, aktivasyonlar, kayıplar, optimizasyon algoritmaları.
- **Dataset ve DataLoader**: veriyi parça parça (mini-batch) vermek.
- Eğitim döngüsü, aşırı öğrenme, başlatma ve normalizasyon, öğrenme oranı.
- Modeli kaydetmek, hata ayıklamak ve uçtan uca bir proje.

Bu patikadaki modeller bilgisayarın işlemcisinde (CPU) çalışıyor ve küçük
tutuldu; her alıştırma birkaç saniyede biter. Büyük modellerde ekran kartı
(GPU) kullanılır, ama fikirler aynıdır.

## Özet

- Derin öğrenme, katman katman öğrenen modellerle ham veriden temsil
  öğrenir.
- PyTorch'ta bir eğitim: veri tensöre, `nn.Sequential` ile model, kayıp
  fonksiyonu, optimizer ve dört adımlı döngü.
- Küçük bir ağ el yazısı rakamları bir saniyenin altında öğrendi; aynı
  veride lojistik regresyon da iyi. Derin öğrenmenin üstünlüğü ham ve
  büyük veride.
