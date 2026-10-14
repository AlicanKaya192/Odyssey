# Üretken Yapay Zekâya Giriş

Bir görüntüden "kedi mi köpek mi" diye karar veren model ile hiç var olmamış
bir kedi resmi çizen model aynı şeyi öğrenmiyor. Birincisi iki sınıfı
**ayırmayı** öğreniyor, ikincisi kedilerin **neye benzediğini**. Bu ikinci
türe **üretken model** (generative model) deniyor; metin yazan, resim çizen,
ses ve kod üreten sistemlerin hepsi bu ailenin üyesi. Bu bölümde ayrımı
küçük, elle tutulur bir örnekle kuracağız: iki balık türünün boy ve ağırlık
ölçüleri. Aynı veriden önce bir sınıflandırıcı, sonra yeni balıklar üreten
bir model kuracağız ve "üretmek" ile "ezberlemek" arasındaki farkı ölçeceğiz.

## İki tür model

<figure class="fig">
  <div class="versus">
    <div class="dim">
      <h5>AYIRT EDİCİ</h5>
<pre><code>model.predict(fish)
# "bream"</code></pre>
      <p>Yalnızca karar verir: bu örnek hangi sınıftan?</p>
    </div>
    <div class="ok">
      <h5>ÜRETKEN</h5>
<pre><code>model.sample("bream")
# [31.2, 546.3]</code></pre>
      <p>Verinin neye benzediğini öğrenir; yeni örnek üretebilir.</p>
    </div>
  </div>
  <figcaption>İkisi de aynı veriden öğrenir; yalnızca üretken model veriyi yeniden oluşturabilir.</figcaption>
</figure>

- **Ayırt edici model** (discriminative model) yalnızca şu soruyu cevaplar:
  "Bu örnek verildiğinde etiket ne?" Matematikte $p(y \mid x)$ yazılır.
  Lojistik regresyon, karar ağacı, metin sınıflandırıcıları bu türdendir.
- **Üretken model** verinin kendisini modeller: "Bu türden bir örnek nasıl
  görünür?" Yani $p(x)$ ya da sınıfa göre $p(x \mid y)$. Bu dağılımı
  öğrendiyse ondan **örnek çekebilir** (sampling): yeni, daha önce
  görmediği ama gerçeğine benzeyen örnekler üretir.

Bugünün büyük dil modelleri de üretken modeldir: metni oluşturan token'ların
dağılımını öğrenir ve sıradaki token'ı bu dağılımdan seçer. Nasıl yaptığını
NLP patikasının ikinci modülünde (Metin Üretimi) sıfırdan yazmıştık; bu
patikada üretken modellerin geri kalanını ve dil modellerinin etrafına
uygulama kurmayı göreceğiz.

## Veri: iki balık türü

`gen_data.py` iki tür balığın (perch ve bream) boyunu (cm) ve ağırlığını (g)
üretiyor. Her çalıştırmada aynı 600 balık geliyor, çünkü üreteç sabit bir
tohum (seed) kullanıyor.

```python
import numpy as np
from gen_data import make_fish

X, y = make_fish()
y = np.array(y)
print(X.shape)
print(X[:3])
for name in ["perch", "bream"]:
    part = X[y == name]
    print(name, len(part), part.mean(axis=0).round(1))
```

```text
(600, 2)
[[ 33.5 595.6]
 [ 31.2 593.4]
 [ 26.6 496.7]]
perch 319 [ 24.  304.5]
bream 281 [ 31.  555.5]
```

Bream ortalamada daha uzun ve daha ağır; ama iki tür örtüşüyor: 26 cm'lik,
450 gramlık bir balık iki türden de olabilir.

## Bir türü bir dağılımla anlatmak

Üretken modelin en basit hâli şu: her türün ölçülerini bir **normal dağılım**
(Gauss dağılımı) ile anlatmak. İki ölçü olduğu için iki boyutlu normal
dağılım kullanıyoruz; onu iki şey belirler:

- **Ortalama vektörü:** türün tipik boyu ve ağırlığı.
- **Kovaryans matrisi:** her ölçünün ne kadar yayıldığı ve iki ölçünün
  birlikte nasıl değiştiği. Uzun balık ağır olur; bu ilişki matrisin köşegen
  dışındaki pozitif sayılarda görünür.

Veriyi önce eğitim ve test diye ayırıyoruz, modeli yalnızca eğitim
balıklarından kuruyoruz:

```python
rng = np.random.default_rng(0)
order = rng.permutation(len(y))
train, test = order[:450], order[450:]


def fit_gaussian(points):
    return points.mean(axis=0), np.cov(points, rowvar=False)


params = {}
for name in ["perch", "bream"]:
    part = X[train][y[train] == name]
    params[name] = fit_gaussian(part)
    mean, cov = params[name]
    print(name, mean.round(1), cov.round(1).tolist())
```

```text
perch [ 24.1 304.4] [[15.5, 197.0], [197.0, 4453.5]]
bream [ 30.8 559.1] [[13.1, 280.2], [280.2, 10012.2]]
```

Tür başına beş sayı (iki ortalama, kovaryansın üç farklı değeri) ve
türlerin oranı bütün "modeli" oluşturuyor. Sinir ağı yok, ama fikir aynı: **veriden bir
dağılım öğrenmek**.

## Aynı model sınıflandırabilir de

Her türün dağılımını bilen biri, yeni bir balığın hangi türe daha çok
benzediğini de söyleyebilir. Bayes kuralıyla: balığın o türün dağılımındaki
**olasılık yoğunluğu** (likelihood) ile türün genel oranı (prior) çarpılır,
büyük olan kazanır. Hesap kolaylığı için logaritmalarla çalışıyoruz.

```python
def log_density(points, mean, cov):
    diff = points - mean
    inv = np.linalg.inv(cov)
    _, logdet = np.linalg.slogdet(cov)
    dist = np.einsum("ij,jk,ik->i", diff, inv, diff)
    return -0.5 * (dist + logdet + 2 * np.log(2 * np.pi))


names = ["perch", "bream"]
scores = []
for name in names:
    prior = np.mean(y[train] == name)
    scores.append(log_density(X[test], *params[name]) + np.log(prior))
pred = np.array(names)[np.argmax(scores, axis=0)]
print("generative:", round(float(np.mean(pred == y[test])), 3))

from sklearn.linear_model import LogisticRegression

clf = LogisticRegression(max_iter=1000).fit(X[train], y[train])
print("logistic:", round(clf.score(X[test], y[test]), 3))
```

```text
generative: 0.9
logistic: 0.88
```

İki model 150 test balığında neredeyse aynı başarıda. Fark başka yerde:
lojistik regresyon yalnızca **karar verir**. Ona "bana bir bream göster"
diyemezsin; içinde balığın neye benzediğine dair bir bilgi yok. Üretken model
ise bunu yapabiliyor.

## Üretmek: dağılımdan örnek çekmek

```python
gen = np.random.default_rng(42)
mean, cov = params["bream"]
new_fish = gen.multivariate_normal(mean, cov, size=5)
print(new_fish.round(1))

many = gen.multivariate_normal(mean, cov, size=1000)
real = X[train][y[train] == "bream"]
print("generated", many.mean(axis=0).round(1), many.std(axis=0).round(1))
print("real     ", real.mean(axis=0).round(1), real.std(axis=0).round(1))
```

```text
[[ 32.4 528.5]
 [ 26.6 484. ]
 [ 39.3 754.2]
 [ 31.2 546.3]
 [ 32.8 560.7]]
generated [ 31.1 566.2] [ 3.7 99.1]
real      [ 30.8 559.1] [ 3.6 99.8]
```

Bu beş balık veride yok; model onları **uydurdu**. Ama rastgele değil:
binlerce örneğin ortalaması ve yayılımı gerçek bream'lere çok yakın.
Üretken bir modeli değerlendirmenin ilk yolu budur: tek tek örneklerin
"doğru" olup olmadığına değil, **üretilenlerin istatistiğinin gerçeğe
benzeyip benzemediğine** bakmak. Çünkü üretimde tek bir doğru cevap yoktur.

## Üretmek mi, ezberlemek mi?

Kolay bir hile var: eğitim verisinden rastgele bir balığı olduğu gibi geri
vermek. İstatistikler mükemmel tutar, ama model hiçbir şey üretmemiştir,
yalnızca **kopyalamıştır**. Gerçek üretken modellerde bu ciddi bir sorun:
eğitim verisindeki bir metni ya da resmi neredeyse aynen geri veren model,
kişisel bilgiyi ya da telifli içeriği sızdırabilir.

Bunu ölçmenin basit bir yolu her üretilen örneğin eğitim verisindeki **en
yakın komşusuna** uzaklığına bakmak. Boy santimetre, ağırlık gram olduğu için
önce iki ölçüyü aynı ölçeğe (standart sapmaya) getiriyoruz:

```python
scale = real.std(axis=0)


def nearest_distance(points, data):
    a = points / scale
    b = data / scale
    d = np.sqrt(((a[:, None, :] - b[None, :, :]) ** 2).sum(axis=2))
    return d.min(axis=1)


copies = real[gen.integers(0, len(real), size=100)]
print("model :", np.median(nearest_distance(many[:100], real)).round(3))
print("copier:", np.median(nearest_distance(copies, real)).round(3))
```

```text
model : 0.089
copier: 0.0
```

Kopyalayan "model"in her örneği bir eğitim balığının tam üstünde (uzaklık
0). Gerçek model yeni noktalar üretiyor; yine de eğitim balıklarına yakın,
çünkü onlardan öğrendi. Sağlıklı bir üretken model ikisinin arasında bir
yerde durur: **gerçeğe benzer, ama kopyası değildir.**

## Üretken modeller neden zor?

Burada iki ölçü ve bir normal dağılım yetti. Bir resmin ise milyonlarca
pikseli var, bir metnin binlerce token'ı. Bu boyutlarda dağılım tek bir
ortalama ve kovaryansla anlatılamaz; bu yüzden üretken modeller farklı
fikirler geliştirdi:

| Fikir | Kısaca | Patikada |
|---|---|---|
| Otomatik kodlayıcı | Veriyi küçük bir koda sıkıştırıp geri açmak | 02 |
| VAE | Kodu bir dağılım yapıp oradan örnek çekmek | 03 |
| GAN | Üretici ile ayırt ediciyi yarıştırmak | 04 |
| Difüzyon | Gürültüyü adım adım temizlemek | 05 |
| Dil modeli | Sıradaki token'ın dağılımını öğrenmek | 06–08 |

Modülün ikinci yarısı dil modellerine ayrılıyor: nasıl üretiyorlar, neden
bazen kendinden emin bir şekilde yanlış söylüyorlar (halüsinasyon), dış
belgelerle nasıl desteklenirler (RAG) ve kendi işimize nasıl uyarlanırlar
(ince ayar, LoRA).

## Özet

- Ayırt edici model $p(y \mid x)$ öğrenir ve karar verir; üretken model
  verinin dağılımını öğrenir ve **yeni örnek üretebilir**.
- En basit üretken model: her sınıfa bir normal dağılım uydurmak. Aynı
  model sınıflandırma da yapabiliyor (Bayes kuralı).
- Üretimde tek doğru cevap yok; üretilenlerin **istatistiği** gerçeğe
  benzemeli.
- İyi model gerçeğe benzer ama **kopyalamaz**; en yakın komşu uzaklığı
  ezberi ölçmenin basit bir yolu.
