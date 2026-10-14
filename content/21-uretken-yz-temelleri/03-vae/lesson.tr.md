# Varyasyonel Otomatik Kodlayıcı

Önceki bölümde otomatik kodlayıcı resimleri iyi sıkıştırdı, ama kod
uzayından yeni resim üretmek zor oldu: kodların nerede durduğunu bilmeden
rastgele nokta seçince çoğu zaman boşluğa düşüyorduk. **Varyasyonel
otomatik kodlayıcı** (variational autoencoder, **VAE**) bu sorunu iki
değişiklikle çözmeye çalışır: kodu tek bir nokta yerine bir **dağılım**
yapar ve bütün kodları aynı, bilinen bir dağılıma (standart normal) doğru
çeker. Böylece "yeni resim için kodu nereden seçeceğim?" sorusunun cevabı
belli olur: standart normalden.

## Veri

Önceki bölümdeki 8×8 rakamlar ve aynı eğitim/test ayrımı:

```python
import numpy as np
from gen_data import load_digit_images

X, y = load_digit_images()
y = np.array(y)
order = np.random.default_rng(0).permutation(len(X))
X_train, X_test = X[order[:1500]], X[order[1500:]]
print(X_train.shape, X_test.shape)
```

```text
(1500, 64) (297, 64)
```

## Fikir: kod bir nokta değil, bir dağılım

<figure class="fig">
  <div class="flow">
    <span class="node">Kodlayıcı</span>
    <span class="arrow">→</span>
    <span class="node acc">μ ve σ</span>
    <span class="arrow">→</span>
    <span class="node ok">z = μ + σ·ε</span>
    <span class="arrow">→</span>
    <span class="node">Kod çözücü</span>
    <span class="arrow">→</span>
    <span class="node acc">Resim</span>
  </div>
  <figcaption>Kodlayıcı bir nokta yerine bir dağılım (merkez μ, yayılım σ) verir; kod çözücüye o dağılımdan çekilen bir örnek gider. ε standart normalden gelen rastgele sayı.</figcaption>
</figure>

Otomatik kodlayıcının kodlayıcısı bir resim için tek bir kod veriyordu.
VAE'nin kodlayıcısı her kod boyutu için **iki sayı** verir:

- **ortalama** $\mu$ (mu): kodun merkezi,
- **log-varyans** $\log \sigma^2$ (`logvar`): kodun ne kadar yayıldığı.
  Doğrudan $\sigma$ yerine logaritmasını öğrenmek, sayının negatif olma
  sorununu ortadan kaldırır: $\sigma = e^{\frac{1}{2}\log\sigma^2}$ her
  zaman pozitif.

Kod çözücüye giden kod bu dağılımdan çekilen bir örnek. Aynı resim her
seferinde biraz farklı bir koda düşer; bu yüzden kod çözücü yalnızca tek
bir noktayı değil, o noktanın **çevresini** de iyi çözmek zorunda kalır.

## Yeniden parametrelendirme hilesi

Rastgele örnek çekmenin türevi alınamaz: "rastgele bir sayı seç" adımı
geriye hata yayamaz. Çözüm, rastgeleliği dışarı almak: önce standart
normalden $\varepsilon$ çek, sonra onu kaydırıp ölçekle:

$$z = \mu + \sigma \cdot \varepsilon, \qquad \varepsilon \sim \mathcal{N}(0, 1)$$

Artık $z$, $\mu$ ve $\sigma$'nın sıradan bir fonksiyonu; türev $\mu$'ye 1,
$\sigma$'ya $\varepsilon$. Buna **yeniden parametrelendirme hilesi**
(reparameterization trick) denir. Doğru dağılımı verdiğini görelim:

```python
rng = np.random.default_rng(0)
mu = np.array([1.5, -0.5])
logvar = np.array([-2.0, 0.0])
std = np.exp(0.5 * logvar)
z = mu + std * rng.normal(size=(10000, 2))
print(z.mean(axis=0).round(2), z.std(axis=0).round(2))
```

```text
[ 1.5 -0.5] [0.37 1.  ]
```

Örneklerin ortalaması $\mu$'ye, yayılımı $\sigma$'ya ($e^{-1} \approx 0{,}37$
ve $e^{0} = 1$) oturuyor.

## Kayıp: geri kurma + KL

VAE'nin kaybı iki terimden oluşur:

1. **Geri kurma terimi:** çıkan resim giren resme benzesin. Pikseller 0–1
   arasında olduğu için **ikili çapraz entropi** (binary cross-entropy)
   kullanıyoruz. Çıkışta `sigmoid` varken bu kaybın türevi çok sade:
   `out - x`.
2. **KL terimi:** her resmin kod dağılımı standart normale yakın olsun.
   İki dağılım arasındaki farkı ölçen **KL ıraksaması** (Kullback–Leibler
   divergence) normal dağılımlar için kapalı bir formül verir:

$$\mathrm{KL} = \frac{1}{2} \sum \left( \mu^2 + \sigma^2 - \log \sigma^2 - 1 \right)$$

```python
def kl_term(mu, logvar):
    return 0.5 * (mu ** 2 + np.exp(logvar) - logvar - 1).sum(axis=-1)


print(kl_term(np.array([0.0, 0.0]), np.array([0.0, 0.0])))
print(kl_term(np.array([2.0, 0.0]), np.array([0.0, 0.0])))
print(kl_term(np.array([0.0, 0.0]), np.array([-2.0, 0.0])).round(3))
```

```text
0.0
2.0
0.568
```

Standart normalin kendisinde KL 0. Merkez 2 birim kayınca KL 2 oluyor:
terim kodları **merkeze çekiyor**. Dağılım daralınca ($\log\sigma^2 = -2$)
KL yine pozitif: terim kodların **tek bir noktaya büzülmesine** de karşı
çıkıyor. İki terim çekişiyor: geri kurma her resme ayrı, dar bir köşe
ister; KL bütün kodları aynı yuvarlak buluta toplar. Toplam kayıp
`geri kurma + beta × KL`; `beta` (β) ikisi arasındaki dengeyi ayarlar.

## Sıfırdan bir VAE

Ağ önceki bölümdekine benziyor: 64 → 32 → kod → 32 → 64. Fark, kodlayıcının
ikiye ayrılan son katmanı (`Wm` ortalamayı, `Wv` log-varyansı veriyor) ve
aradaki örnekleme. Ağırlıkları **Adam** ile güncelliyoruz (İleri Matematik
modülünün Gradyan İnişi bölümü): momentum, ayrıca her ağırlık için kendi
adım boyu. Momentumla denediğimizde KL terimi kodları bir anda tek noktaya
yapıştırdı ve ağ hiçbir şey öğrenmedi; Adam ile eğitim düzgün ilerledi.

Türevler el ile yazıldı: KL'nin türevi $\mu$'ye göre $\mu$, $\log\sigma^2$'ye
göre $\frac{1}{2}(\sigma^2 - 1)$; örnekleme adımından gelen türev $\mu$'ye
aynen, $\log\sigma^2$'ye $\varepsilon \cdot \frac{1}{2}\sigma$ ile çarpılarak
geçiyor.

```python
def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def encode(x, P):
    h = np.tanh(x @ P["W1"] + P["b1"])
    return h, h @ P["Wm"] + P["bm"], h @ P["Wv"] + P["bv"]


def decode(z, P):
    g = np.tanh(z @ P["W3"] + P["b3"])
    return g, sigmoid(g @ P["W4"] + P["b4"])


def train_vae(data, k, beta=1.0, steps=1500, lr=0.01, seed=0):
    rng = np.random.default_rng(seed)
    sizes = {"W1": (64, 32), "Wm": (32, k), "Wv": (32, k),
             "W3": (k, 32), "W4": (32, 64)}
    P = {}
    for name, (a, b) in sizes.items():
        P[name] = rng.normal(0, np.sqrt(1 / a), (a, b))
        P["b" + name[1:]] = np.zeros(b)
    m = {name: 0 * p for name, p in P.items()}
    v = {name: 0 * p for name, p in P.items()}
    n = len(data)
    for t in range(1, steps + 1):
        h, mu, logvar = encode(data, P)
        std = np.exp(0.5 * logvar)
        eps = rng.normal(size=mu.shape)
        z = mu + std * eps
        g, out = decode(z, P)
        d_out = (out - data) / n
        d_g = d_out @ P["W4"].T * (1 - g ** 2)
        d_z = d_g @ P["W3"].T
        d_mu = d_z + beta * mu / n
        d_lv = d_z * eps * 0.5 * std + beta * 0.5 * (std ** 2 - 1) / n
        d_h = (d_mu @ P["Wm"].T + d_lv @ P["Wv"].T) * (1 - h ** 2)
        grads = {"W4": g.T @ d_out, "b4": d_out.sum(0),
                 "W3": z.T @ d_g, "b3": d_g.sum(0),
                 "Wm": h.T @ d_mu, "bm": d_mu.sum(0),
                 "Wv": h.T @ d_lv, "bv": d_lv.sum(0),
                 "W1": data.T @ d_h, "b1": d_h.sum(0)}
        for name, grad in grads.items():
            m[name] = 0.9 * m[name] + 0.1 * grad
            v[name] = 0.999 * v[name] + 0.001 * grad ** 2
            m_hat = m[name] / (1 - 0.9 ** t)
            v_hat = v[name] / (1 - 0.999 ** t)
            P[name] = P[name] - lr * m_hat / (np.sqrt(v_hat) + 1e-8)
    return P


models = {}
for beta in [0.0, 1.0]:
    P = train_vae(X_train, 2, beta)
    models[beta] = P
    _, mu, logvar = encode(X_test, P)
    error = ((X_test - decode(mu, P)[1]) ** 2).mean()
    print("beta", beta, "error", error.round(4),
          "KL", kl_term(mu, logvar).mean().round(2))
    print("  code mean", mu.mean(axis=0).round(2),
          "std", mu.std(axis=0).round(2))
```

```text
beta 0.0 error 0.0381 KL 79.37
  code mean [-9.99  1.69] std [3.95 4.46]
beta 1.0 error 0.0346 KL 2.82
  code mean [-0.02  0.04] std [1.03 0.97]
```

`beta = 0` olunca KL terimi yok ve model sıradan bir otomatik kodlayıcıya
dönüyor: kodların merkezi ve yayılımı ağın keyfine kalmış, sıfırdan uzak
bir yerde ve geniş. `beta = 1` olunca kodların ortalaması 0'a, yayılımı
1'e oturuyor; KL terimi kod uzayını standart normalin şekline sokmuş.
Test resimlerini geri kurarken kodun merkezini ($\mu$) kullanıyoruz,
örnek çekmiyoruz.

## Kod uzayı haritası

2 sayılık kodun her noktasını çözüp ızgara hâlinde dizersek modelin "kod
uzayında ne öğrendiğini" görürüz. İki modelde de aynı bölgeyi,
$-2$ ile $2$ arasını tarıyoruz:

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="539.300625pt" height="288.637734pt" viewBox="0 0 539.300625 288.637734" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 288.637734 
L 539.300625 288.637734 
L 539.300625 0 
L 0 0 
L 0 288.637734 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 42.942969 250.436953 
L 271.061797 250.436953 
L 271.061797 22.318125 
L 42.942969 22.318125 
L 42.942969 250.436953 
z
" style="fill: none"/>
   </g>
   <g clip-path="url(#p0ae7c27617)">
    <image xlink:href="data:image/png;base64,
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" id="image08f3d40f33" transform="scale(1 -1) translate(0 -228.24)" x="43.2" y="-22.237734" width="227.52" height="228.24"/>
   </g>
   <g id="matplotlib.axis_1">
    <g id="xtick_1">
     <g id="line2d_1">
      <defs>
       <path id="m15aed4d867" d="M 0 0 
L 0 3.5 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m15aed4d867" x="57.387174" y="250.436953" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="57.387174" y="265.034609" transform="rotate(-0 57.387174 265.034609)">−2</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="107.194778" y="250.436953" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="107.194778" y="265.034609" transform="rotate(-0 107.194778 265.034609)">−1</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="157.002383" y="250.436953" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="157.002383" y="265.034609" transform="rotate(-0 157.002383 265.034609)">0</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="206.809987" y="250.436953" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="206.809987" y="265.034609" transform="rotate(-0 206.809987 265.034609)">1</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="256.617592" y="250.436953" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="256.617592" y="265.034609" transform="rotate(-0 256.617592 265.034609)">2</text>
     </g>
    </g>
    <g id="text_6">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="157.002383" y="279.035391" transform="rotate(-0 157.002383 279.035391)">code 1</text>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_6">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="42.942969" y="235.992748" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="35.942969" y="239.791576" transform="rotate(-0 35.942969 239.791576)">−2</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m5c8d5162d3" x="42.942969" y="186.185143" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="35.942969" y="189.983972" transform="rotate(-0 35.942969 189.983972)">−1</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="42.942969" y="136.377539" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="35.942969" y="140.176367" transform="rotate(-0 35.942969 140.176367)">0</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="42.942969" y="86.569935" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="35.942969" y="90.368763" transform="rotate(-0 35.942969 90.368763)">1</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="42.942969" y="36.76233" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="35.942969" y="40.561158" transform="rotate(-0 35.942969 40.561158)">2</text>
     </g>
    </g>
    <g id="text_12">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="136.377539" transform="rotate(-90 14.798438 136.377539)">code 2</text>
    </g>
   </g>
   <g id="patch_3">
    <path d="M 42.942969 250.436953 
L 42.942969 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 271.061797 250.436953 
L 271.061797 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 42.942969 250.436953 
L 271.061797 250.436953 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 42.942969 22.318125 
L 271.061797 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_13">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="157.002383" y="16.318125" transform="rotate(-0 157.002383 16.318125)">autoencoder</text>
   </g>
  </g>
  <g id="axes_2">
   <g id="patch_7">
    <path d="M 303.981797 250.436953 
L 532.100625 250.436953 
L 532.100625 22.318125 
L 303.981797 22.318125 
L 303.981797 250.436953 
z
" style="fill: none"/>
   </g>
   <g clip-path="url(#p35363c60c5)">
    <image xlink:href="data:image/png;base64,
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" id="image00c6118817" transform="scale(1 -1) translate(0 -228.24)" x="303.84" y="-22.237734" width="228.24" height="228.24"/>
   </g>
   <g id="matplotlib.axis_3">
    <g id="xtick_6">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m15aed4d867" x="318.426002" y="250.436953" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="318.426002" y="265.034609" transform="rotate(-0 318.426002 265.034609)">−2</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m15aed4d867" x="368.233607" y="250.436953" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_15">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="368.233607" y="265.034609" transform="rotate(-0 368.233607 265.034609)">−1</text>
     </g>
    </g>
    <g id="xtick_8">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m15aed4d867" x="418.041211" y="250.436953" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_16">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="418.041211" y="265.034609" transform="rotate(-0 418.041211 265.034609)">0</text>
     </g>
    </g>
    <g id="xtick_9">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m15aed4d867" x="467.848815" y="250.436953" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_17">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="467.848815" y="265.034609" transform="rotate(-0 467.848815 265.034609)">1</text>
     </g>
    </g>
    <g id="xtick_10">
     <g id="line2d_15">
      <g>
       <use xlink:href="#m15aed4d867" x="517.65642" y="250.436953" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_18">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="517.65642" y="265.034609" transform="rotate(-0 517.65642 265.034609)">2</text>
     </g>
    </g>
    <g id="text_19">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="418.041211" y="279.035391" transform="rotate(-0 418.041211 279.035391)">code 1</text>
    </g>
   </g>
   <g id="matplotlib.axis_4">
    <g id="ytick_6">
     <g id="line2d_16">
      <g>
       <use xlink:href="#m5c8d5162d3" x="303.981797" y="235.992748" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_20">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="296.981797" y="239.791576" transform="rotate(-0 296.981797 239.791576)">−2</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_17">
      <g>
       <use xlink:href="#m5c8d5162d3" x="303.981797" y="186.185143" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_21">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="296.981797" y="189.983972" transform="rotate(-0 296.981797 189.983972)">−1</text>
     </g>
    </g>
    <g id="ytick_8">
     <g id="line2d_18">
      <g>
       <use xlink:href="#m5c8d5162d3" x="303.981797" y="136.377539" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_22">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="296.981797" y="140.176367" transform="rotate(-0 296.981797 140.176367)">0</text>
     </g>
    </g>
    <g id="ytick_9">
     <g id="line2d_19">
      <g>
       <use xlink:href="#m5c8d5162d3" x="303.981797" y="86.569935" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_23">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="296.981797" y="90.368763" transform="rotate(-0 296.981797 90.368763)">1</text>
     </g>
    </g>
    <g id="ytick_10">
     <g id="line2d_20">
      <g>
       <use xlink:href="#m5c8d5162d3" x="303.981797" y="36.76233" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_24">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="296.981797" y="40.561158" transform="rotate(-0 296.981797 40.561158)">2</text>
     </g>
    </g>
   </g>
   <g id="patch_8">
    <path d="M 303.981797 250.436953 
L 303.981797 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_9">
    <path d="M 532.100625 250.436953 
L 532.100625 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_10">
    <path d="M 303.981797 250.436953 
L 532.100625 250.436953 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_11">
    <path d="M 303.981797 22.318125 
L 532.100625 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_25">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="418.041211" y="16.318125" transform="rotate(-0 418.041211 16.318125)">VAE</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p0ae7c27617">
   <rect x="42.942969" y="22.318125" width="228.118828" height="228.118828"/>
  </clipPath>
  <clipPath id="p35363c60c5">
   <rect x="303.981797" y="22.318125" width="228.118828" height="228.118828"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Kod uzayında −2 ile 2 arasındaki 8 × 8 noktanın çözülmüş hâli. Solda otomatik kodlayıcı (β = 0), sağda VAE (β = 1). Aynı bölge VAE'de farklı rakamlarla dolu; otomatik kodlayıcıda birkaç rakam ve rakama benzemeyen lekeler var.</figcaption>
</figure>

VAE'nin haritasında rakamlar birbirine yumuşakça geçiyor ve bölgenin her
yerinde bir rakam var. Otomatik kodlayıcının kodları başka bir yerde
durduğu için aynı bölgede yalnızca birkaç rakam var; sağ yarısı rakama
benzemeyen dolu lekeler.

## Standart normalden yeni rakamlar

Şimdi asıl sınav: iki modelde de standart normalden 1000 kod çekip
çözüyoruz ve önceki bölümün hakemine (gerçek resimlerle eğitilmiş lojistik
regresyon) soruyoruz. Hakemin tahminine göre her rakamdan kaç resim
çıktığını sayıyoruz; en az %5'i (50 resmi) bulan rakamı "görüldü"
sayıyoruz:

```python
from sklearn.linear_model import LogisticRegression

judge = LogisticRegression(max_iter=2000).fit(X_train, y[order[:1500]])
z = np.random.default_rng(1).normal(size=(1000, 2))
for name, beta in [("autoencoder", 0.0), ("VAE", 1.0)]:
    images = decode(z, models[beta])[1]
    counts = np.bincount(judge.predict(images), minlength=10)
    sure = judge.predict_proba(images).max(axis=1) > 0.9
    print(name, counts)
    print("  digits seen", (counts >= 50).sum(), "sure", sure.mean().round(3))
```

```text
autoencoder [  0 500   2   0 217   0  88   0 193   0]
  digits seen 4 sure 0.262
VAE [100 100  98 149 104  62  94 113  96  84]
  digits seen 10 sure 0.333
```

Otomatik kodlayıcıdan çekilen kodlar yalnızca birkaç rakam üretiyor;
geri kalanlar kod uzayının başka bir köşesinde ve standart normal oraya
hiç uğramıyor. VAE'de on rakamın hepsi çıkıyor. Bu sonuç tek bir
başlangıca bağlı değil: eğitimi iki farklı tohumla daha tekrarladığımızda
otomatik kodlayıcı 3 ve 5 rakam, VAE yine 10 rakam verdi.

Dikkat: hakemin "çok emin" olduğu oran bu çalıştırmada VAE'de biraz
yüksek, ama tohumdan tohuma değişiyor ve öteki iki tohumda otomatik
kodlayıcıda daha yüksek çıktı (tohum 1: otomatik kodlayıcı 0,49, VAE 0,356; tohum 2: otomatik kodlayıcı 0,435, VAE 0,367). Yani VAE tek tek
resimleri daha net yapmıyor. Kazancı başka yerde: **nereden örnek
çekeceğimizi biliyoruz** ve oradan çekince bütün türler çıkıyor.

## Bedeli ve β dengesi

Kod 2 sayıyken VAE'nin geri kurma hatası otomatik kodlayıcınınkinden bile
biraz düşük çıktı (0,0346'ya karşı 0,0381); yani bedel her zaman
görünmüyor. Kod büyüyünce görünüyor:

```python
for beta in [0.0, 1.0]:
    P = train_vae(X_train, 8, beta)
    _, mu, _ = encode(X_test, P)
    error = ((X_test - decode(mu, P)[1]) ** 2).mean()
    print("code 8, beta", beta, "error", error.round(4))
```

```text
code 8, beta 0.0 error 0.0139
code 8, beta 1.0 error 0.025
```

8 sayılık kodda otomatik kodlayıcının hatası VAE'ninkinin yaklaşık
yarısı. KL terimi her kodu standart normale doğru çektiği için VAE ayrıntıyı
kodda o kadar serbestçe saklayamıyor ve daha bulanık geri kuruyor. β bu
dengeyi ayarlıyor:

```python
for beta in [0.25, 1.0, 4.0]:
    P = train_vae(X_train, 2, beta)
    _, mu, logvar = encode(X_test, P)
    error = ((X_test - decode(mu, P)[1]) ** 2).mean()
    counts = np.bincount(judge.predict(decode(z, P)[1]), minlength=10)
    print("beta", beta, "error", error.round(4),
          "KL", kl_term(mu, logvar).mean().round(2),
          "digits", (counts >= 50).sum())
```

```text
beta 0.25 error 0.0336 KL 4.9 digits 9
beta 1.0 error 0.0346 KL 2.82 digits 10
beta 4.0 error 0.0744 KL 0.0 digits 1
```

β büyüdükçe KL düşüyor (kodlar standart normale daha çok benziyor) ve
geri kurma hatası artıyor. β = 4'te KL sıfıra iniyor: kodlar standart
normalin kendisi olmuş, resim hakkında hiçbir bilgi taşımıyor ve model
bütün kodlardan neredeyse aynı resmi çıkarıyor (tek rakam). Buna **sonsal çöküş**
(posterior collapse) denir. Öbür uçta, β = 0,25'te KL 4,9'a çıkıyor ve
rakamlardan biri artık 50 resme ulaşamıyor: kod uzayı otomatik kodlayıcıya
doğru kayıyor.

## VAE'nin yeri

- Kod uzayı düzenli olduğu için iki kodun arasındaki doğru üzerinde
  ilerlemek (**ara değerleme**, interpolation) haritadaki gibi bir rakamdan
  ötekine geçiş verir.
- VAE'nin resimleri bulanık kalır; daha keskin resim için sonraki
  bölümlerde GAN ve difüzyon modellerini göreceğiz.
- Modern resim üreticilerinin çoğu üretimi doğrudan piksellerde değil, bir
  VAE'nin küçük kod uzayında yapar ve en sonda VAE'nin kod çözücüsüyle resmi
  büyütür.

## Özet

- VAE'nin kodlayıcısı her resim için bir dağılım ($\mu$, $\log\sigma^2$)
  verir; kod bu dağılımdan $z = \mu + \sigma\varepsilon$ ile çekilir.
- Kayıp = geri kurma + β × KL. KL kodları standart normale çeker.
- `beta = 0` sıradan otomatik kodlayıcıdır; kodları sıfırdan uzakta ve
  geniş bir alanda durur.
- Standart normalden çekilen kodlarla otomatik kodlayıcı 10 rakamın
  birkaçını, VAE hepsini üretti (üç farklı başlangıçta da).
- Bedeli: kod büyüyünce daha bulanık geri kurma (8 sayılık kodda 0,0139'a
  karşı 0,025). β ikisi arasındaki dengeyi ayarlar; çok büyük β'da model
  çöker.
