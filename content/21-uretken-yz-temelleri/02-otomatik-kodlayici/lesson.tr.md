# Otomatik Kodlayıcı

İlk bölümde bir balığı iki sayıyla (boy, ağırlık) anlattık ve iki boyutlu bir
dağılım yetti. Bir resim ise yüzlerce, binlerce sayıdan oluşur ve bu
sayıların çoğu birbirine bağlıdır: bir rakamın çizgisi rastgele piksellerden
değil, birkaç "fikirden" (eğim, kalınlık, halka var mı) oluşur. **Otomatik
kodlayıcı** (autoencoder) bu fikirleri bulmaya çalışır: resmi küçük bir
**koda** sıkıştırır, sonra koddan resmi geri kurar. Bu bölümde önce doğrusal
yolu (PCA) görecek, sonra NumPy ile sıfırdan bir otomatik kodlayıcı
eğitecek ve kod uzayından yeni resim üretmeye çalışacağız. O deneme, bir
sonraki bölümün (VAE) neden gerektiğini gösterecek.

## Veri: 8×8 el yazısı rakamlar

scikit-learn'ün içinde gelen 1797 küçük rakam resmi kullanıyoruz; internet
gerekmiyor. Her resim 8×8 = 64 piksel, piksel değeri 0 (beyaz) ile 1
(siyah) arasında.

```python
import numpy as np
from gen_data import load_digit_images

X, y = load_digit_images()
y = np.array(y)
order = np.random.default_rng(0).permutation(len(X))
X_train, X_test = X[order[:1500]], X[order[1500:]]
print(X.shape, X_train.shape, X_test.shape)
print(X[0].reshape(8, 8).round(1)[2])
```

```text
(1797, 64) (1500, 64) (297, 64)
[0.  0.2 0.9 0.1 0.  0.7 0.5 0. ]
```

Son satır ilk resmin (bir 0) üçüncü piksel satırı: ortadaki boşluk ve iki
yandaki çizgi görünüyor.

## Fikir: dar boğaz

<figure class="fig">
  <div class="flow">
    <span class="node acc">Resim<br>64 piksel</span>
    <span class="arrow">→</span>
    <span class="node">Kodlayıcı</span>
    <span class="arrow">→</span>
    <span class="node ok">Kod<br>2–8 sayı</span>
    <span class="arrow">→</span>
    <span class="node">Kod çözücü</span>
    <span class="arrow">→</span>
    <span class="node acc">Resim<br>64 piksel</span>
  </div>
  <figcaption>Dar boğaz: 64 sayı birkaç sayıya iner ve oradan geri kurulur. Hedef, çıkanın girene benzemesi.</figcaption>
</figure>

Otomatik kodlayıcının iki parçası var:

- **Kodlayıcı** (encoder): 64 pikseli birkaç sayılık bir **koda** indirir.
- **Kod çözücü** (decoder): koddan 64 pikseli geri kurar.

Eğitimde tek hedef var: çıkan resim giren resme benzesin. Kod dar olduğu
için ağ her şeyi ezberleyemez; resimler arasında **ortak olanı** öğrenmek
zorunda kalır. Etiket kullanılmıyor: hangi resmin hangi rakam olduğunu ağ
hiç görmüyor. Bu yüzden otomatik kodlayıcı **denetimsiz** (unsupervised)
bir yöntem.

## Doğrusal yol: PCA

En basit "kodlayıcı" doğrusal bir izdüşüm: veriyi en çok yayıldığı $k$ yöne
yansıtmak. Bu, ML patikasından tanıdığın **PCA** (temel bileşenler analizi).
Kodu geri açmak da aynı yönlerle çarpmak:

```python
mean = X_train.mean(axis=0)
_, _, Vt = np.linalg.svd(X_train - mean, full_matrices=False)
for k in [2, 8, 16, 32]:
    code = (X_test - mean) @ Vt[:k].T
    rebuilt = code @ Vt[:k] + mean
    print(k, ((X_test - rebuilt) ** 2).mean().round(4))
```

```text
2 0.0539
8 0.0245
16 0.0115
32 0.0026
```

Kod büyüdükçe hata düşüyor: 32 sayı, 64 pikseli neredeyse kusursuz geri
kuruyor. Ama PCA'nın sınırı doğrusal olması: rakamların şekli düz
yönlerle anlatılamayacak kadar eğri olabilir.

## Sinir ağıyla otomatik kodlayıcı

Doğrusal olmayan bir otomatik kodlayıcıyı NumPy ile kuruyoruz: katman
boyutları 64 → 32 → kod → 32 → 64. Gizli katmanlarda `tanh`, çıkışta
piksellerin 0–1 aralığında kalması için `sigmoid` var. Eğitim, ML
Algoritmaları'ndaki sinir ağıyla aynı: ileri hesap, hatanın türevini geriye
yaymak (geri yayılım), ağırlıkları biraz düzeltmek. Adımlar hızlı ilerlesin
diye **momentum** ekledik: her güncelleme bir önceki güncellemenin bir
kısmını taşıyor.

```python
def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def layers(x, weights, start=0):
    acts = [x]
    for i, (W, b) in enumerate(weights[start:], start):
        z = acts[-1] @ W + b
        acts.append(sigmoid(z) if i == 3 else np.tanh(z))
    return acts


def train_autoencoder(data, code_size, epochs=3000, lr=0.05, seed=0):
    rng = np.random.default_rng(seed)
    sizes = [64, 32, code_size, 32, 64]
    weights = [(rng.normal(0, np.sqrt(1 / a), (a, b)), np.zeros(b))
               for a, b in zip(sizes, sizes[1:])]
    speed = [(np.zeros_like(W), np.zeros_like(b)) for W, b in weights]
    for _ in range(epochs):
        acts = layers(data, weights)
        out = acts[-1]
        grad = 2 * (out - data) / len(data) * out * (1 - out)
        for i in reversed(range(4)):
            W, b = weights[i]
            gW, gb = acts[i].T @ grad, grad.sum(axis=0)
            if i:
                grad = grad @ W.T * (1 - acts[i] ** 2)
            vW = 0.9 * speed[i][0] - lr * gW
            vb = 0.9 * speed[i][1] - lr * gb
            speed[i] = (vW, vb)
            weights[i] = (W + vW, b + vb)
    return weights


for k in [2, 8]:
    model = train_autoencoder(X_train, k)
    rebuilt = layers(X_test, model)[-1]
    print(k, ((X_test - rebuilt) ** 2).mean().round(4))
```

```text
2 0.0393
8 0.0156
```

Aynı kod boyunda doğrusal olmayan otomatik kodlayıcı PCA'dan belirgin
biçimde iyi: 2 sayılık kodda hata 0,0539'dan 0,0393'e, 8 sayılıkta
0,0245'ten 0,0156'ya iniyor. Bedeli eğitim: PCA tek bir SVD, bu ağ 3000
adım ve bu bilgisayarda birkaç saniye sürüyor. Uzun eğitimde küçük
hesap farkları büyüdüğü için başka bir bilgisayarda son basamaklar biraz
farklı çıkabilir.

`layers(x, weights[:2])` yalnızca kodlayıcıyı çalıştırıp kodu,
`layers(code, weights, start=2)` yalnızca kod çözücüyü çalıştırıp resmi
veriyor; ikisini aşağıda ayrı ayrı kullanacağız.

## Kod uzayı

2 sayılık kodun güzel bir yanı var: her resmi düzlemde bir nokta olarak
çizebiliriz. Ağa etiket hiç verilmediği hâlde aynı rakamlar bir arada
toplanıyor:

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="452.96375pt" height="294.878437pt" viewBox="0 0 452.96375 294.878437" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 294.878437 
L 452.96375 294.878437 
L 452.96375 0 
L 0 0 
L 0 294.878437 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 58.846094 256.677656 
L 445.76375 256.677656 
L 445.76375 7.2 
L 58.846094 7.2 
L 58.846094 256.677656 
z
" style="fill: none"/>
   </g>
   <g id="PathCollection_1">
    <defs>
     <path id="ma80715a32c" d="M 0 1.581139 
C 0.419323 1.581139 0.821528 1.41454 1.118034 1.118034 
C 1.41454 0.821528 1.581139 0.419323 1.581139 0 
C 1.581139 -0.419323 1.41454 -0.821528 1.118034 -1.118034 
C 0.821528 -1.41454 0.419323 -1.581139 0 -1.581139 
C -0.419323 -1.581139 -0.821528 -1.41454 -1.118034 -1.118034 
C -1.41454 -0.821528 -1.581139 -0.419323 -1.581139 0 
C -1.581139 0.419323 -1.41454 0.821528 -1.118034 1.118034 
C -0.821528 1.41454 -0.419323 1.581139 0 1.581139 
z
" style="stroke: #1f77b4"/>
    </defs>
    <g clip-path="url(#p8353f94a05)">
     <use xlink:href="#ma80715a32c" x="349.972561" y="19.613224" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="414.252592" y="18.634985" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="262.822887" y="18.911846" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="296.261528" y="18.555624" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="405.080421" y="18.733636" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="372.798894" y="18.559313" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="310.22511" y="18.634923" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="328.199489" y="18.640156" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="379.214577" y="18.685423" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="348.401474" y="18.644756" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="368.443546" y="18.679329" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="368.173516" y="18.721095" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="365.828129" y="18.539893" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="305.805484" y="18.622866" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="311.4378" y="22.041806" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="394.539835" y="18.567918" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="327.888106" y="18.548252" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="296.287431" y="18.551496" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="398.846951" y="18.635921" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="347.481125" y="18.582929" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="349.541737" y="18.883869" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="370.5673" y="18.644594" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="310.74192" y="18.572012" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="333.788385" y="18.552301" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="321.564063" y="18.556053" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="334.135517" y="18.611504" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="320.835429" y="211.943624" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="303.381083" y="18.571047" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="266.969766" y="19.36474" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="294.702697" y="18.556152" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="299.556815" y="19.026221" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="374.747487" y="56.94964" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#ma80715a32c" x="343.53183" y="18.648566" style="fill: #1f77b4; stroke: #1f77b4"/>
    </g>
   </g>
   <g id="PathCollection_2">
    <defs>
     <path id="m2f7684cc0a" d="M 0 1.581139 
C 0.419323 1.581139 0.821528 1.41454 1.118034 1.118034 
C 1.41454 0.821528 1.581139 0.419323 1.581139 0 
C 1.581139 -0.419323 1.41454 -0.821528 1.118034 -1.118034 
C 0.821528 -1.41454 0.419323 -1.581139 0 -1.581139 
C -0.419323 -1.581139 -0.821528 -1.41454 -1.118034 -1.118034 
C -1.41454 -0.821528 -1.581139 -0.419323 -1.581139 0 
C -1.581139 0.419323 -1.41454 0.821528 -1.118034 1.118034 
C -0.821528 1.41454 -0.419323 1.581139 0 1.581139 
z
" style="stroke: #ff7f0e"/>
    </defs>
    <g clip-path="url(#p8353f94a05)">
     <use xlink:href="#m2f7684cc0a" x="77.066472" y="42.497198" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="421.73602" y="202.951926" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="344.353218" y="197.363077" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="422.405113" y="211.728461" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="426.885456" y="208.238111" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="79.688396" y="18.59535" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="364.177931" y="202.526668" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="329.891496" y="215.356103" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="79.243983" y="24.964662" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="326.73373" y="216.291003" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="357.070663" y="220.312775" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="332.096165" y="217.68026" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="425.974209" y="203.198798" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="228.00244" y="201.860916" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="80.082433" y="84.571358" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="339.245478" y="218.399725" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="320.208416" y="217.340291" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="341.180131" y="219.386716" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="412.18351" y="226.312653" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="251.107439" y="184.350936" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="356.23128" y="197.365751" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="303.535037" y="207.638025" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="322.557444" y="205.879835" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="269.525068" y="198.303449" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="287.660113" y="200.998259" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="325.942666" y="210.648446" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="77.653199" y="47.197185" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="106.247415" y="145.784825" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="325.680119" y="207.548139" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="138.156453" y="115.476014" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="77.844001" y="43.552392" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="343.825032" y="218.747054" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m2f7684cc0a" x="340.903486" y="218.673054" style="fill: #ff7f0e; stroke: #ff7f0e"/>
    </g>
   </g>
   <g id="PathCollection_3">
    <defs>
     <path id="mb6880ae3ae" d="M 0 1.581139 
C 0.419323 1.581139 0.821528 1.41454 1.118034 1.118034 
C 1.41454 0.821528 1.581139 0.419323 1.581139 0 
C 1.581139 -0.419323 1.41454 -0.821528 1.118034 -1.118034 
C 0.821528 -1.41454 0.419323 -1.581139 0 -1.581139 
C -0.419323 -1.581139 -0.821528 -1.41454 -1.118034 -1.118034 
C -1.41454 -0.821528 -1.581139 -0.419323 -1.581139 0 
C -1.581139 0.419323 -1.41454 0.821528 -1.118034 1.118034 
C -0.821528 1.41454 -0.419323 1.581139 0 1.581139 
z
" style="stroke: #2ca02c"/>
    </defs>
    <g clip-path="url(#p8353f94a05)">
     <use xlink:href="#mb6880ae3ae" x="422.845167" y="173.006013" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="406.368964" y="155.291723" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="409.614757" y="182.953489" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="400.188119" y="161.78461" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="376.630684" y="152.053074" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="425.12289" y="183.179443" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="419.255424" y="176.831163" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="395.616495" y="167.95985" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="397.265156" y="179.890224" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="392.524515" y="189.22559" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="416.921755" y="189.632835" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="424.394274" y="199.140319" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="423.071801" y="164.812224" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="311.181994" y="188.963759" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="374.693379" y="192.461284" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="419.474965" y="184.585978" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="338.433462" y="164.931753" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="427.912537" y="177.958631" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="418.523747" y="162.304687" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="426.634598" y="186.245994" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="371.101727" y="171.54905" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="400.570611" y="179.691011" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="409.567102" y="193.283557" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="178.392379" y="211.646034" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="411.838467" y="175.766228" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="261.695935" y="211.38102" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="392.928216" y="169.974182" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="417.624432" y="194.910951" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="389.611385" y="161.260284" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="419.822349" y="179.49885" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="413.452887" y="174.435475" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="360.593301" y="161.83976" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="370.704699" y="170.741976" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="422.240651" y="159.062866" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="423.222261" y="121.988767" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="394.386633" y="172.913533" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="386.440501" y="187.985898" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="283.424842" y="209.381317" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="413.08216" y="166.08237" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="428.176584" y="186.436712" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="382.823309" y="187.470447" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#mb6880ae3ae" x="422.037994" y="175.818909" style="fill: #2ca02c; stroke: #2ca02c"/>
    </g>
   </g>
   <g id="PathCollection_4">
    <defs>
     <path id="m192783d34b" d="M 0 1.581139 
C 0.419323 1.581139 0.821528 1.41454 1.118034 1.118034 
C 1.41454 0.821528 1.581139 0.419323 1.581139 0 
C 1.581139 -0.419323 1.41454 -0.821528 1.118034 -1.118034 
C 0.821528 -1.41454 0.419323 -1.581139 0 -1.581139 
C -0.419323 -1.581139 -0.821528 -1.41454 -1.118034 -1.118034 
C -1.41454 -0.821528 -1.581139 -0.419323 -1.581139 0 
C -1.581139 0.419323 -1.41454 0.821528 -1.118034 1.118034 
C -0.821528 1.41454 -0.419323 1.581139 0 1.581139 
z
" style="stroke: #d62728"/>
    </defs>
    <g clip-path="url(#p8353f94a05)">
     <use xlink:href="#m192783d34b" x="392.360986" y="72.279387" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m192783d34b" x="366.903214" y="92.97817" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m192783d34b" x="382.219672" y="98.606371" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m192783d34b" x="361.050427" y="97.40958" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m192783d34b" x="369.440417" y="118.500934" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m192783d34b" x="344.366646" y="102.496054" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m192783d34b" x="381.871616" y="95.254798" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m192783d34b" x="279.748247" y="169.933418" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m192783d34b" x="311.222782" y="105.260138" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m192783d34b" x="373.511523" y="98.164298" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m192783d34b" x="328.183165" y="122.232668" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m192783d34b" x="364.084946" y="120.823169" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m192783d34b" x="324.912285" y="111.242742" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m192783d34b" x="376.029536" y="99.648138" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m192783d34b" x="389.557364" y="93.751013" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m192783d34b" x="337.043019" y="131.136498" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m192783d34b" x="358.801908" y="109.233602" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m192783d34b" x="370.950464" y="92.248098" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m192783d34b" x="369.436085" y="98.882231" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m192783d34b" x="404.645826" y="69.063791" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m192783d34b" x="379.750676" y="119.472988" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m192783d34b" x="366.987033" y="104.458845" style="fill: #d62728; stroke: #d62728"/>
    </g>
   </g>
   <g id="PathCollection_5">
    <defs>
     <path id="ma829a29230" d="M 0 1.581139 
C 0.419323 1.581139 0.821528 1.41454 1.118034 1.118034 
C 1.41454 0.821528 1.581139 0.419323 1.581139 0 
C 1.581139 -0.419323 1.41454 -0.821528 1.118034 -1.118034 
C 0.821528 -1.41454 0.419323 -1.581139 0 -1.581139 
C -0.419323 -1.581139 -0.821528 -1.41454 -1.118034 -1.118034 
C -1.41454 -0.821528 -1.581139 -0.419323 -1.581139 0 
C -1.581139 0.419323 -1.41454 0.821528 -1.118034 1.118034 
C -0.821528 1.41454 -0.419323 1.581139 0 1.581139 
z
" style="stroke: #9467bd"/>
    </defs>
    <g clip-path="url(#p8353f94a05)">
     <use xlink:href="#ma829a29230" x="77.964541" y="210.752023" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="157.669342" y="238.319166" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="88.517178" y="245.337536" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="140.033497" y="245.330945" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="153.270479" y="231.345858" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="154.31638" y="233.31562" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="151.945515" y="222.167197" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="82.662953" y="204.11413" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="77.085116" y="209.319666" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="83.987928" y="242.283773" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="129.063004" y="245.326184" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="95.622119" y="245.33668" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="171.975386" y="236.02786" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="78.223679" y="245.322434" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="118.488773" y="245.336875" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="111.993974" y="245.337763" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="125.086579" y="239.569839" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="116.513966" y="240.516255" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="263.669608" y="232.460983" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="81.674826" y="245.337672" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="81.533751" y="160.432293" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="146.612904" y="236.271667" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="136.95556" y="236.86435" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="116.149636" y="245.333921" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="170.807356" y="232.07928" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="185.574679" y="236.662412" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="98.049416" y="233.764726" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="78.206166" y="245.335882" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="216.887273" y="193.566197" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="94.839426" y="220.710449" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="145.502084" y="245.323946" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="158.879924" y="235.179778" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="161.457697" y="232.184711" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="208.712448" y="245.33692" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="161.929288" y="245.323268" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="171.756996" y="171.160073" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#ma829a29230" x="162.972043" y="243.23807" style="fill: #9467bd; stroke: #9467bd"/>
    </g>
   </g>
   <g id="PathCollection_6">
    <defs>
     <path id="me9f8ebc3b1" d="M 0 1.581139 
C 0.419323 1.581139 0.821528 1.41454 1.118034 1.118034 
C 1.41454 0.821528 1.581139 0.419323 1.581139 0 
C 1.581139 -0.419323 1.41454 -0.821528 1.118034 -1.118034 
C 0.821528 -1.41454 0.419323 -1.581139 0 -1.581139 
C -0.419323 -1.581139 -0.821528 -1.41454 -1.118034 -1.118034 
C -1.41454 -0.821528 -1.581139 -0.419323 -1.581139 0 
C -1.581139 0.419323 -1.41454 0.821528 -1.118034 1.118034 
C -0.821528 1.41454 -0.419323 1.581139 0 1.581139 
z
" style="stroke: #8c564b"/>
    </defs>
    <g clip-path="url(#p8353f94a05)">
     <use xlink:href="#me9f8ebc3b1" x="234.872092" y="60.955524" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="199.428097" y="110.202124" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="180.558173" y="162.84569" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="218.831255" y="183.623728" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="208.927367" y="125.624912" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="387.52486" y="63.511817" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="294.951463" y="51.964182" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="180.045844" y="172.102853" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="253.488812" y="68.437263" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="351.850445" y="59.428297" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="219.41726" y="73.094046" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="197.943956" y="49.014381" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="230.528535" y="56.235282" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="180.450107" y="173.377257" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="189.438611" y="171.771763" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="280.97644" y="157.628653" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="200.315722" y="74.494859" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="248.270934" y="132.836714" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="214.972046" y="84.629543" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="190.706645" y="173.577832" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="188.061954" y="166.611243" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="186.573868" y="163.076172" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="212.165761" y="68.600344" style="fill: #8c564b; stroke: #8c564b"/>
     <use xlink:href="#me9f8ebc3b1" x="172.043158" y="138.154353" style="fill: #8c564b; stroke: #8c564b"/>
    </g>
   </g>
   <g id="PathCollection_7">
    <defs>
     <path id="m6eadb44be7" d="M 0 1.581139 
C 0.419323 1.581139 0.821528 1.41454 1.118034 1.118034 
C 1.41454 0.821528 1.581139 0.419323 1.581139 0 
C 1.581139 -0.419323 1.41454 -0.821528 1.118034 -1.118034 
C 0.821528 -1.41454 0.419323 -1.581139 0 -1.581139 
C -0.419323 -1.581139 -0.821528 -1.41454 -1.118034 -1.118034 
C -1.41454 -0.821528 -1.581139 -0.419323 -1.581139 0 
C -1.581139 0.419323 -1.41454 0.821528 -1.118034 1.118034 
C -0.821528 1.41454 -0.419323 1.581139 0 1.581139 
z
" style="stroke: #e377c2"/>
    </defs>
    <g clip-path="url(#p8353f94a05)">
     <use xlink:href="#m6eadb44be7" x="369.789284" y="243.822123" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="318.649381" y="245.330047" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="303.207899" y="245.336315" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="361.024266" y="245.332314" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="334.774499" y="245.334875" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="367.376326" y="245.268743" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="380.32942" y="245.337014" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="271.071477" y="212.863557" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="314.173468" y="245.330296" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="324.442534" y="244.536052" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="336.032916" y="245.330548" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="392.245823" y="245.337329" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="298.696918" y="244.781936" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="291.377891" y="244.240719" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="335.175279" y="245.223139" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="364.62472" y="232.178499" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="392.873524" y="236.426585" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="335.048488" y="244.802395" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="311.682578" y="245.329982" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="408.782011" y="226.613914" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="247.463926" y="210.389955" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="394.861724" y="245.33745" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="370.906511" y="245.33643" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="324.191214" y="245.337197" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="385.796668" y="245.332648" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="306.726716" y="245.336795" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="299.143642" y="245.321085" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="352.669986" y="245.299468" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="288.269252" y="245.329809" style="fill: #e377c2; stroke: #e377c2"/>
     <use xlink:href="#m6eadb44be7" x="293.358275" y="245.323166" style="fill: #e377c2; stroke: #e377c2"/>
    </g>
   </g>
   <g id="PathCollection_8">
    <defs>
     <path id="mab7770e5c8" d="M 0 1.581139 
C 0.419323 1.581139 0.821528 1.41454 1.118034 1.118034 
C 1.41454 0.821528 1.581139 0.419323 1.581139 0 
C 1.581139 -0.419323 1.41454 -0.821528 1.118034 -1.118034 
C 0.821528 -1.41454 0.419323 -1.581139 0 -1.581139 
C -0.419323 -1.581139 -0.821528 -1.41454 -1.118034 -1.118034 
C -1.41454 -0.821528 -1.581139 -0.419323 -1.581139 0 
C -1.581139 0.419323 -1.41454 0.821528 -1.118034 1.118034 
C -0.821528 1.41454 -0.419323 1.581139 0 1.581139 
z
" style="stroke: #7f7f7f"/>
    </defs>
    <g clip-path="url(#p8353f94a05)">
     <use xlink:href="#mab7770e5c8" x="189.822569" y="211.460963" style="fill: #7f7f7f; stroke: #7f7f7f"/>
     <use xlink:href="#mab7770e5c8" x="95.523567" y="196.638025" style="fill: #7f7f7f; stroke: #7f7f7f"/>
     <use xlink:href="#mab7770e5c8" x="161.83694" y="207.213604" style="fill: #7f7f7f; stroke: #7f7f7f"/>
     <use xlink:href="#mab7770e5c8" x="108.325047" y="200.643423" style="fill: #7f7f7f; stroke: #7f7f7f"/>
     <use xlink:href="#mab7770e5c8" x="153.244915" y="209.457851" style="fill: #7f7f7f; stroke: #7f7f7f"/>
     <use xlink:href="#mab7770e5c8" x="185.991457" y="205.876863" style="fill: #7f7f7f; stroke: #7f7f7f"/>
     <use xlink:href="#mab7770e5c8" x="140.618705" y="200.164457" style="fill: #7f7f7f; stroke: #7f7f7f"/>
     <use xlink:href="#mab7770e5c8" x="175.598342" y="216.938097" style="fill: #7f7f7f; stroke: #7f7f7f"/>
     <use xlink:href="#mab7770e5c8" x="84.018075" y="189.320652" style="fill: #7f7f7f; stroke: #7f7f7f"/>
     <use xlink:href="#mab7770e5c8" x="207.801864" y="227.873506" style="fill: #7f7f7f; stroke: #7f7f7f"/>
     <use xlink:href="#mab7770e5c8" x="76.43326" y="143.001792" style="fill: #7f7f7f; stroke: #7f7f7f"/>
     <use xlink:href="#mab7770e5c8" x="77.055432" y="170.204496" style="fill: #7f7f7f; stroke: #7f7f7f"/>
     <use xlink:href="#mab7770e5c8" x="237.768459" y="212.779582" style="fill: #7f7f7f; stroke: #7f7f7f"/>
     <use xlink:href="#mab7770e5c8" x="142.339053" y="201.098901" style="fill: #7f7f7f; stroke: #7f7f7f"/>
     <use xlink:href="#mab7770e5c8" x="136.405044" y="180.50207" style="fill: #7f7f7f; stroke: #7f7f7f"/>
     <use xlink:href="#mab7770e5c8" x="127.645115" y="197.089664" style="fill: #7f7f7f; stroke: #7f7f7f"/>
     <use xlink:href="#mab7770e5c8" x="155.52003" y="198.708292" style="fill: #7f7f7f; stroke: #7f7f7f"/>
     <use xlink:href="#mab7770e5c8" x="108.579925" y="197.248438" style="fill: #7f7f7f; stroke: #7f7f7f"/>
     <use xlink:href="#mab7770e5c8" x="204.157034" y="214.951084" style="fill: #7f7f7f; stroke: #7f7f7f"/>
     <use xlink:href="#mab7770e5c8" x="212.962888" y="221.792677" style="fill: #7f7f7f; stroke: #7f7f7f"/>
     <use xlink:href="#mab7770e5c8" x="208.895676" y="208.660928" style="fill: #7f7f7f; stroke: #7f7f7f"/>
     <use xlink:href="#mab7770e5c8" x="204.486971" y="224.791778" style="fill: #7f7f7f; stroke: #7f7f7f"/>
     <use xlink:href="#mab7770e5c8" x="175.985703" y="204.000665" style="fill: #7f7f7f; stroke: #7f7f7f"/>
    </g>
   </g>
   <g id="PathCollection_9">
    <defs>
     <path id="mcbc9253283" d="M 0 1.581139 
C 0.419323 1.581139 0.821528 1.41454 1.118034 1.118034 
C 1.41454 0.821528 1.581139 0.419323 1.581139 0 
C 1.581139 -0.419323 1.41454 -0.821528 1.118034 -1.118034 
C 0.821528 -1.41454 0.419323 -1.581139 0 -1.581139 
C -0.419323 -1.581139 -0.821528 -1.41454 -1.118034 -1.118034 
C -1.41454 -0.821528 -1.581139 -0.419323 -1.581139 0 
C -1.581139 0.419323 -1.41454 0.821528 -1.118034 1.118034 
C -0.821528 1.41454 -0.419323 1.581139 0 1.581139 
z
" style="stroke: #bcbd22"/>
    </defs>
    <g clip-path="url(#p8353f94a05)">
     <use xlink:href="#mcbc9253283" x="340.702017" y="105.701164" style="fill: #bcbd22; stroke: #bcbd22"/>
     <use xlink:href="#mcbc9253283" x="226.154478" y="194.525215" style="fill: #bcbd22; stroke: #bcbd22"/>
     <use xlink:href="#mcbc9253283" x="183.3723" y="111.9566" style="fill: #bcbd22; stroke: #bcbd22"/>
     <use xlink:href="#mcbc9253283" x="277.966655" y="177.386507" style="fill: #bcbd22; stroke: #bcbd22"/>
     <use xlink:href="#mcbc9253283" x="350.127408" y="189.18094" style="fill: #bcbd22; stroke: #bcbd22"/>
     <use xlink:href="#mcbc9253283" x="333.29102" y="173.378204" style="fill: #bcbd22; stroke: #bcbd22"/>
     <use xlink:href="#mcbc9253283" x="321.159397" y="192.276721" style="fill: #bcbd22; stroke: #bcbd22"/>
     <use xlink:href="#mcbc9253283" x="274.637196" y="173.933556" style="fill: #bcbd22; stroke: #bcbd22"/>
     <use xlink:href="#mcbc9253283" x="319.291802" y="105.264173" style="fill: #bcbd22; stroke: #bcbd22"/>
     <use xlink:href="#mcbc9253283" x="260.869453" y="174.560981" style="fill: #bcbd22; stroke: #bcbd22"/>
     <use xlink:href="#mcbc9253283" x="309.498113" y="116.435044" style="fill: #bcbd22; stroke: #bcbd22"/>
     <use xlink:href="#mcbc9253283" x="317.373461" y="103.131481" style="fill: #bcbd22; stroke: #bcbd22"/>
     <use xlink:href="#mcbc9253283" x="292.873485" y="178.55838" style="fill: #bcbd22; stroke: #bcbd22"/>
     <use xlink:href="#mcbc9253283" x="316.011069" y="167.734111" style="fill: #bcbd22; stroke: #bcbd22"/>
     <use xlink:href="#mcbc9253283" x="297.354067" y="138.084142" style="fill: #bcbd22; stroke: #bcbd22"/>
     <use xlink:href="#mcbc9253283" x="315.144988" y="96.84404" style="fill: #bcbd22; stroke: #bcbd22"/>
     <use xlink:href="#mcbc9253283" x="270.458992" y="108.077736" style="fill: #bcbd22; stroke: #bcbd22"/>
     <use xlink:href="#mcbc9253283" x="283.84672" y="178.664479" style="fill: #bcbd22; stroke: #bcbd22"/>
     <use xlink:href="#mcbc9253283" x="78.111028" y="108.451191" style="fill: #bcbd22; stroke: #bcbd22"/>
     <use xlink:href="#mcbc9253283" x="295.823435" y="173.881349" style="fill: #bcbd22; stroke: #bcbd22"/>
     <use xlink:href="#mcbc9253283" x="294.77749" y="169.1959" style="fill: #bcbd22; stroke: #bcbd22"/>
     <use xlink:href="#mcbc9253283" x="315.410678" y="161.862581" style="fill: #bcbd22; stroke: #bcbd22"/>
    </g>
   </g>
   <g id="PathCollection_10">
    <defs>
     <path id="mf52eed36ec" d="M 0 1.581139 
C 0.419323 1.581139 0.821528 1.41454 1.118034 1.118034 
C 1.41454 0.821528 1.581139 0.419323 1.581139 0 
C 1.581139 -0.419323 1.41454 -0.821528 1.118034 -1.118034 
C 0.821528 -1.41454 0.419323 -1.581139 0 -1.581139 
C -0.419323 -1.581139 -0.821528 -1.41454 -1.118034 -1.118034 
C -1.41454 -0.821528 -1.581139 -0.419323 -1.581139 0 
C -1.581139 0.419323 -1.41454 0.821528 -1.118034 1.118034 
C -0.821528 1.41454 -0.419323 1.581139 0 1.581139 
z
" style="stroke: #17becf"/>
    </defs>
    <g clip-path="url(#p8353f94a05)">
     <use xlink:href="#mf52eed36ec" x="308.594225" y="27.616296" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="327.339923" y="71.746056" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="399.542466" y="61.161203" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="76.660829" y="52.71024" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="353.724752" y="43.759605" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="76.541784" y="238.621961" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="294.95488" y="63.506862" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="288.180565" y="53.025536" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="76.86822" y="19.641948" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="274.42877" y="124.615041" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="333.14244" y="39.456835" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="371.952671" y="59.782721" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="360.916422" y="64.787253" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="397.344658" y="55.458968" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="309.897332" y="83.372196" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="357.840066" y="58.2055" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="377.087099" y="57.763649" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="365.054479" y="61.836473" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="330.683012" y="89.696" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="250.890198" y="21.926716" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="377.94016" y="62.127432" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="306.964393" y="77.909729" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="76.437624" y="133.944124" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="76.789054" y="19.542104" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="381.786795" y="48.516504" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="363.564368" y="64.332455" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="77.28355" y="51.012704" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="389.965902" y="62.476773" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="381.576506" y="60.014774" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="411.822358" y="69.187492" style="fill: #17becf; stroke: #17becf"/>
     <use xlink:href="#mf52eed36ec" x="408.32355" y="66.307524" style="fill: #17becf; stroke: #17becf"/>
    </g>
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
       <use xlink:href="#m15aed4d867" x="76.235044" y="256.677656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="76.235044" y="271.275312" transform="rotate(-0 76.235044 271.275312)">−1.00</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="120.688654" y="256.677656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="120.688654" y="271.275312" transform="rotate(-0 120.688654 271.275312)">−0.75</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="165.142263" y="256.677656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="165.142263" y="271.275312" transform="rotate(-0 165.142263 271.275312)">−0.50</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="209.595873" y="256.677656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="209.595873" y="271.275312" transform="rotate(-0 209.595873 271.275312)">−0.25</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="254.049483" y="256.677656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="254.049483" y="271.275312" transform="rotate(-0 254.049483 271.275312)">0.00</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="298.503092" y="256.677656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="298.503092" y="271.275312" transform="rotate(-0 298.503092 271.275312)">0.25</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m15aed4d867" x="342.956702" y="256.677656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="342.956702" y="271.275312" transform="rotate(-0 342.956702 271.275312)">0.50</text>
     </g>
    </g>
    <g id="xtick_8">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m15aed4d867" x="387.410311" y="256.677656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="387.410311" y="271.275312" transform="rotate(-0 387.410311 271.275312)">0.75</text>
     </g>
    </g>
    <g id="xtick_9">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m15aed4d867" x="431.863921" y="256.677656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="431.863921" y="271.275312" transform="rotate(-0 431.863921 271.275312)">1.00</text>
     </g>
    </g>
    <g id="text_10">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="252.304922" y="285.276094" transform="rotate(-0 252.304922 285.276094)">code 1</text>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_10">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="58.846094" y="245.337954" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="51.846094" y="249.136782" transform="rotate(-0 51.846094 249.136782)">−1.00</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="58.846094" y="216.987824" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="51.846094" y="220.786653" transform="rotate(-0 51.846094 220.786653)">−0.75</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="58.846094" y="188.637695" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="51.846094" y="192.436523" transform="rotate(-0 51.846094 192.436523)">−0.50</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m5c8d5162d3" x="58.846094" y="160.287565" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="51.846094" y="164.086393" transform="rotate(-0 51.846094 164.086393)">−0.25</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m5c8d5162d3" x="58.846094" y="131.937435" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_15">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="51.846094" y="135.736264" transform="rotate(-0 51.846094 135.736264)">0.00</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_15">
      <g>
       <use xlink:href="#m5c8d5162d3" x="58.846094" y="103.587306" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_16">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="51.846094" y="107.386134" transform="rotate(-0 51.846094 107.386134)">0.25</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_16">
      <g>
       <use xlink:href="#m5c8d5162d3" x="58.846094" y="75.237176" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_17">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="51.846094" y="79.036004" transform="rotate(-0 51.846094 79.036004)">0.50</text>
     </g>
    </g>
    <g id="ytick_8">
     <g id="line2d_17">
      <g>
       <use xlink:href="#m5c8d5162d3" x="58.846094" y="46.887047" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_18">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="51.846094" y="50.685875" transform="rotate(-0 51.846094 50.685875)">0.75</text>
     </g>
    </g>
    <g id="ytick_9">
     <g id="line2d_18">
      <g>
       <use xlink:href="#m5c8d5162d3" x="58.846094" y="18.536917" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_19">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="51.846094" y="22.335745" transform="rotate(-0 51.846094 22.335745)">1.00</text>
     </g>
    </g>
    <g id="text_20">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798437" y="131.938828" transform="rotate(-90 14.798437 131.938828)">code 2</text>
    </g>
   </g>
   <g id="patch_3">
    <path d="M 58.846094 256.677656 
L 58.846094 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 445.76375 256.677656 
L 445.76375 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 58.846094 256.677656 
L 445.76375 256.677656 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 58.846094 7.2 
L 445.76375 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_21">
    <text style="font-weight: 700; font-size: 14px; font-family:inherit; text-anchor: middle; fill: currentColor" x="338.667439" y="29.454468" transform="rotate(-0 338.667439 29.454468)">0</text>
   </g>
   <g id="text_22">
    <text style="font-weight: 700; font-size: 14px; font-family:inherit; text-anchor: middle; fill: currentColor" x="279.851334" y="177.931853" transform="rotate(-0 279.851334 177.931853)">1</text>
   </g>
   <g id="text_23">
    <text style="font-weight: 700; font-size: 14px; font-family:inherit; text-anchor: middle; fill: currentColor" x="390.009836" y="181.168429" transform="rotate(-0 390.009836 181.168429)">2</text>
   </g>
   <g id="text_24">
    <text style="font-weight: 700; font-size: 14px; font-family:inherit; text-anchor: middle; fill: currentColor" x="360.594447" y="109.231125" transform="rotate(-0 360.594447 109.231125)">3</text>
   </g>
   <g id="text_25">
    <text style="font-weight: 700; font-size: 14px; font-family:inherit; text-anchor: middle; fill: currentColor" x="133.961932" y="235.032027" transform="rotate(-0 133.961932 235.032027)">4</text>
   </g>
   <g id="text_26">
    <text style="font-weight: 700; font-size: 14px; font-family:inherit; text-anchor: middle; fill: currentColor" x="225.930975" y="117.878337" transform="rotate(-0 225.930975 117.878337)">5</text>
   </g>
   <g id="text_27">
    <text style="font-weight: 700; font-size: 14px; font-family:inherit; text-anchor: middle; fill: currentColor" x="335.825554" y="245.206732" transform="rotate(-0 335.825554 245.206732)">6</text>
   </g>
   <g id="text_28">
    <text style="font-weight: 700; font-size: 14px; font-family:inherit; text-anchor: middle; fill: currentColor" x="155.261568" y="205.394015" transform="rotate(-0 155.261568 205.394015)">7</text>
   </g>
   <g id="text_29">
    <text style="font-weight: 700; font-size: 14px; font-family:inherit; text-anchor: middle; fill: currentColor" x="285.19342" y="153.595105" transform="rotate(-0 285.19342 153.595105)">8</text>
   </g>
   <g id="text_30">
    <text style="font-weight: 700; font-size: 14px; font-family:inherit; text-anchor: middle; fill: currentColor" x="296.26126" y="70.219386" transform="rotate(-0 296.26126 70.219386)">9</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p8353f94a05">
   <rect x="58.846094" y="7.2" width="386.917656" height="249.477656"/>
  </clipPath>
 </defs>
</svg>
<figcaption>297 test resminin 2 sayılık kodu; renk ve büyük rakam gerçek etiketi gösteriyor. Ağ etiketleri hiç görmedi, yine de aynı rakamlar bir arada; kümeler arasında boşluklar var.</figcaption>
</figure>

Bu, otomatik kodlayıcının veriden anlamlı bir yapı çıkardığını gösteriyor.
Ama resme dikkatli bak: rakam kümelerinin arasında **boşluklar** var ve
kümeler farklı genişlikte.

## Koddan yeni resim üretmek

Kod çözücü elimizde: bir kod verirsek bir resim çıkarıyor. Yeni bir rakam
üretmek için kod uzayından rastgele bir nokta seçip kod çözücüye versek?
Bunu ölçelim. Test resimlerinin kodlarının kapladığı kutudan düzgün
rastgele kodlar çekip çözüyoruz. Çıkan resimlerin "rakama benzeyip
benzemediğini" bir **hakem** söylesin: gerçek resimlerle eğitilmiş bir
lojistik regresyon. Hakemin bir resim için %90'dan fazla emin olduğu oranı
üç grupta karşılaştırıyoruz:

```python
model2 = train_autoencoder(X_train, 2)
codes = layers(X_test, model2[:2])[-1]
low, high = codes.min(axis=0), codes.max(axis=0)
random_codes = np.random.default_rng(1).uniform(low, high, size=(297, 2))
from_random = layers(random_codes, model2, start=2)[-1]
from_real = layers(codes, model2, start=2)[-1]

from sklearn.linear_model import LogisticRegression

judge = LogisticRegression(max_iter=2000).fit(X_train, y[order[:1500]])
groups = [("test images ", X_test), ("real codes  ", from_real),
          ("random codes", from_random)]
for name, images in groups:
    sure = judge.predict_proba(images).max(axis=1)
    print(name, (sure > 0.9).mean().round(3))
```

```text
test images  0.694
real codes   0.539
random codes 0.316
```

Hakem gerçek test resimlerinin %69'unda, gerçek kodlardan geri kurulan
resimlerin %54'ünde çok emin; rastgele kodlardan çıkan resimlerin ise
yalnızca %32'sinde. Kutunun içindeki pek çok nokta hiçbir rakamın
düşmediği boşluklara denk geliyor ve oradan çıkan resim iki rakamın bulanık
bir karışımı oluyor. Otomatik kodlayıcı **sıkıştırmayı** öğrendi, ama kod
uzayının **hangi bölgesinin "geçerli"** olduğunu bilmiyor. Bu yüzden iyi
bir üretken model sayılmaz.

Çözüm bir sonraki bölümün konusu: kodu tek bir nokta yerine bir **dağılım**
yapmak ve kod uzayını düzenli olmaya zorlamak. Bu modele **varyasyonel
otomatik kodlayıcı** (VAE) deniyor.

## Otomatik kodlayıcı ne işe yarar?

Üretken model olarak zayıf olsa da otomatik kodlayıcı çok kullanılır:

- **Boyut indirgeme ve görselleştirme:** yüksek boyutlu veriyi 2–3 sayıya
  indirip çizmek.
- **Gürültü temizleme** (denoising): gürültülü resmi kodlayıp çözünce
  gürültünün çoğu gider, çünkü kod yalnızca ortak yapıyı taşıyor.
- **Aykırı değer bulma** (anomaly detection): eğitimde görülmeyen türden bir
  örnek kötü geri kurulur; yüksek hata "bu farklı" demektir.
- **Büyük modellerin içinde:** modern resim üreticilerinin çoğu, resmi önce
  bir otomatik kodlayıcıyla küçük bir koda indirir ve üretimi o kod
  uzayında yapar; en sonda kod çözücü resmi büyütür.

## Özet

- Otomatik kodlayıcı veriyi dar bir koda sıkıştırıp geri kurar; etiket
  kullanmaz.
- PCA doğrusal bir otomatik kodlayıcı gibidir: tek SVD, kod büyüdükçe hata
  düşer.
- Doğrusal olmayan ağ aynı kod boyunda daha iyi geri kurar (2 boyutta
  0,0539 → 0,0393).
- Kod uzayında aynı türden örnekler bir araya toplanır, ama aralarda
  boşluklar vardır.
- Rastgele bir koddan üretilen resimlerin çok azı net bir rakamdır (%32,
  gerçeklerde %69): otomatik kodlayıcı iyi bir üretici değildir. Çözüm VAE.
