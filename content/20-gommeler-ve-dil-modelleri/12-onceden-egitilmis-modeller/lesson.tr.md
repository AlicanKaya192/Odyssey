# Önceden Eğitilmiş Modeller

Etiketli veri pahalıdır: bir insanın binlerce talebi tek tek okuyup
kategorisini yazması gerekir. Etiketsiz metin ise boldur. **Ön eğitim**
(pretraining) bu dengesizlikten yararlanır: model önce bol etiketsiz metinde,
etiket gerektirmeyen bir görevle (kelimenin bağlamını, sonraki kelimeyi ya
da gizlenen kelimeyi tahmin etmek) dilin yapısını öğrenir. Sonra bu bilgi,
az etiketli asıl göreve **aktarılır** (transfer learning). Bu fikrin en
küçük hâlini 01'den beri kullanıyoruz: kelime vektörleri etiketsiz metinden
öğrenildi. Büyük dil modelleri aynı fikrin milyarlarca kelimeyle ve
transformer bloklarıyla büyütülmüş hâli. Bu bölümde ön eğitimin **neyi
kazandırdığını** ölçeceğiz.

## Etiketsiz metinden ön eğitim

20 000 destek talebi; kategorileri **kullanmıyoruz**, yalnızca metinleri.
Yöntem 04'teki PPMI + SVD.

```python
import re
from collections import Counter
import numpy as np
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from text_data import make_tickets

TOKEN = re.compile(r"[a-z]+")


def pretrain(texts, dims=50):
    docs = [TOKEN.findall(t.lower()) for t in texts]
    counts = Counter(w for d in docs for w in d)
    vocab = sorted(w for w in counts if counts[w] >= 3)
    index = {w: i for i, w in enumerate(vocab)}
    M = np.zeros((len(vocab), len(vocab)))
    for d in docs:
        ids = [index.get(w) for w in d]
        for i, a in enumerate(ids):
            for j in range(max(0, i - 4), min(len(ids), i + 5)):
                if a is not None and j != i and ids[j] is not None:
                    M[a, ids[j]] += 1
    with np.errstate(divide="ignore", invalid="ignore"):
        P = np.log(M * M.sum() / np.outer(M.sum(1), M.sum(0)))
    U, S, _ = np.linalg.svd(np.nan_to_num(np.maximum(P, 0)))
    E = U[:, :dims] * S[:dims]
    return index, E / np.linalg.norm(E, axis=1, keepdims=True)


unlabelled = [t["text"] for t in make_tickets(20000, seed=1)]
index, E = pretrain(unlabelled)
print(len(index), E.shape)
```

```text
440 (440, 50)
```

440 kelimenin her biri için 50 sayı. Bu vektörler hiçbir etiket görmedi.

## Az etiketle öğrenmek

Şimdi etiketli 3000 talep: ilk 2000'i etiket havuzu, son 1000'i sınav.
Havuzdan rastgele `n` talep seçip iki sınıflandırıcı eğitiyoruz:

- **TF-IDF + lojistik regresyon**: yalnızca o `n` talepten öğrenir.
- **Ön eğitimli vektörler + lojistik regresyon**: talebin vektörü,
  kelimelerinin ön eğitimli vektörlerinin ortalaması (04'teki gibi).

Tek bir rastgele seçime güvenmemek için her `n`'de 5 farklı seçimin
ortalamasını alıyoruz.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


def embed(text):
    words = [w for w in TOKEN.findall(text.lower())
             if w in index and w not in ENGLISH_STOP_WORDS]
    if not words:
        return np.zeros(E.shape[1])
    v = np.mean([E[index[w]] for w in words], axis=0)
    return v / np.linalg.norm(v)


tickets = make_tickets(3000)
texts = [t["text"] for t in tickets]
y = np.array([t["category"] for t in tickets])
pool, test = np.arange(2000), np.arange(2000, 3000)
D = np.array([embed(t) for t in texts])
test_texts = [texts[i] for i in test]


def curve_point(n):
    lexical, pretrained = [], []
    for seed in range(5):
        pick = np.random.default_rng(seed).choice(pool, n, replace=False)
        picked = [texts[i] for i in pick]
        tfidf = TfidfVectorizer(stop_words="english").fit(picked)
        lr = LogisticRegression(max_iter=1000)
        lr.fit(tfidf.transform(picked), y[pick])
        lexical.append(np.mean(lr.predict(tfidf.transform(test_texts)) == y[test]))
        lr = LogisticRegression(max_iter=1000, C=10).fit(D[pick], y[pick])
        pretrained.append(np.mean(lr.predict(D[test]) == y[test]))
    return round(float(np.mean(lexical)), 3), round(float(np.mean(pretrained)), 3)


for n in [10, 20, 50, 100, 300, 1000, 2000]:
    print(n, *curve_point(n))
```

```text
10 0.353 0.551
20 0.623 0.748
50 0.749 0.866
100 0.889 0.914
300 0.937 0.941
1000 0.956 0.951
2000 0.961 0.953
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="394.423125pt" height="235.698344pt" viewBox="0 0 394.423125 235.698344" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 235.698344 
L 394.423125 235.698344 
L 394.423125 0 
L 0 0 
L 0 235.698344 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 30.103125 195.696 
L 387.223125 195.696 
L 387.223125 7.2 
L 30.103125 7.2 
L 30.103125 195.696 
z
" style="fill: none"/>
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
       <use xlink:href="#m15aed4d867" x="46.335852" y="195.696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <g style="fill: currentColor" transform="translate(37.535852 211.996)">
       <text>
        <tspan x="0" y="-0.762187" style="font-size: 10px; font-family:inherit; fill: currentColor">1</tspan>
        <tspan x="6.362305" y="-0.762187" style="font-size: 10px; font-family:inherit; fill: currentColor">0</tspan>
        <tspan x="12.820312" y="-4.892187" style="font-size: 7px; font-family:inherit; fill: currentColor">1</tspan>
       </text>
      </g>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="187.426819" y="195.696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <g style="fill: currentColor" transform="translate(178.626819 212.096)">
       <text>
        <tspan x="0" y="-0.674688" style="font-size: 10px; font-family:inherit; fill: currentColor">1</tspan>
        <tspan x="6.362305" y="-0.674688" style="font-size: 10px; font-family:inherit; fill: currentColor">0</tspan>
        <tspan x="12.820312" y="-4.804688" style="font-size: 7px; font-family:inherit; fill: currentColor">2</tspan>
       </text>
      </g>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="328.517785" y="195.696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <g style="fill: currentColor" transform="translate(319.717785 212.096)">
       <text>
        <tspan x="0" y="-0.674688" style="font-size: 10px; font-family:inherit; fill: currentColor">1</tspan>
        <tspan x="6.362305" y="-0.674688" style="font-size: 10px; font-family:inherit; fill: currentColor">0</tspan>
        <tspan x="12.820312" y="-4.804688" style="font-size: 7px; font-family:inherit; fill: currentColor">3</tspan>
       </text>
      </g>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <defs>
       <path id="m4926b1a248" d="M 0 0 
L 0 2 
" style="stroke: currentColor; stroke-width: 0.6"/>
      </defs>
      <g>
       <use xlink:href="#m4926b1a248" x="32.662725" y="195.696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m4926b1a248" x="39.879884" y="195.696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m4926b1a248" x="88.808465" y="195.696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m4926b1a248" x="113.653351" y="195.696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_8">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m4926b1a248" x="131.281078" y="195.696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_9">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m4926b1a248" x="144.954206" y="195.696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_10">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m4926b1a248" x="156.125964" y="195.696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_11">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m4926b1a248" x="165.571551" y="195.696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_12">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m4926b1a248" x="173.753691" y="195.696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_13">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m4926b1a248" x="180.97085" y="195.696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_14">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m4926b1a248" x="229.899431" y="195.696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_15">
     <g id="line2d_15">
      <g>
       <use xlink:href="#m4926b1a248" x="254.744317" y="195.696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_16">
     <g id="line2d_16">
      <g>
       <use xlink:href="#m4926b1a248" x="272.372044" y="195.696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_17">
     <g id="line2d_17">
      <g>
       <use xlink:href="#m4926b1a248" x="286.045172" y="195.696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_18">
     <g id="line2d_18">
      <g>
       <use xlink:href="#m4926b1a248" x="297.21693" y="195.696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_19">
     <g id="line2d_19">
      <g>
       <use xlink:href="#m4926b1a248" x="306.662518" y="195.696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_20">
     <g id="line2d_20">
      <g>
       <use xlink:href="#m4926b1a248" x="314.844657" y="195.696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_21">
     <g id="line2d_21">
      <g>
       <use xlink:href="#m4926b1a248" x="322.061816" y="195.696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_22">
     <g id="line2d_22">
      <g>
       <use xlink:href="#m4926b1a248" x="370.990398" y="195.696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="text_4">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="208.663125" y="226.096" transform="rotate(-0 208.663125 226.096)">n</text>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_23">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="173.881421" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="177.680249" transform="rotate(-0 23.103125 177.680249)">0.4</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_24">
      <g>
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="145.697211" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="149.496039" transform="rotate(-0 23.103125 149.496039)">0.5</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_25">
      <g>
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="117.513" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="121.311828" transform="rotate(-0 23.103125 121.311828)">0.6</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_26">
      <g>
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="89.328789" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="93.127618" transform="rotate(-0 23.103125 93.127618)">0.7</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_27">
      <g>
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="61.144579" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="64.943407" transform="rotate(-0 23.103125 64.943407)">0.8</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_28">
      <g>
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="32.960368" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="36.759197" transform="rotate(-0 23.103125 36.759197)">0.9</text>
     </g>
    </g>
   </g>
   <g id="line2d_29">
    <path d="M 46.335852 187.128 
L 88.808465 111.030632 
L 144.954206 75.518526 
L 187.426819 36.060632 
L 254.744317 22.532211 
L 328.517785 17.177211 
L 370.990398 15.768 
" clip-path="url(#pd066cb7d0a)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
    <defs>
     <path id="m98ae7f93d8" d="M 0 3 
C 0.795609 3 1.55874 2.683901 2.12132 2.12132 
C 2.683901 1.55874 3 0.795609 3 0 
C 3 -0.795609 2.683901 -1.55874 2.12132 -2.12132 
C 1.55874 -2.683901 0.795609 -3 0 -3 
C -0.795609 -3 -1.55874 -2.683901 -2.12132 -2.12132 
C -2.683901 -1.55874 -3 -0.795609 -3 0 
C -3 0.795609 -2.683901 1.55874 -2.12132 2.12132 
C -1.55874 2.683901 -0.795609 3 0 3 
z
" style="stroke: #1f77b4"/>
    </defs>
    <g clip-path="url(#pd066cb7d0a)">
     <use xlink:href="#m98ae7f93d8" x="46.335852" y="187.128" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="88.808465" y="111.030632" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="144.954206" y="75.518526" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="187.426819" y="36.060632" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="254.744317" y="22.532211" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="328.517785" y="17.177211" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="370.990398" y="15.768" style="fill: #1f77b4; stroke: #1f77b4"/>
    </g>
   </g>
   <g id="line2d_30">
    <path d="M 46.335852 131.323263 
L 88.808465 75.800368 
L 144.954206 42.543 
L 187.426819 29.014579 
L 254.744317 21.404842 
L 328.517785 18.586421 
L 370.990398 18.022737 
" clip-path="url(#pd066cb7d0a)" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linecap: square"/>
    <defs>
     <path id="m43dc4bf304" d="M 0 3 
C 0.795609 3 1.55874 2.683901 2.12132 2.12132 
C 2.683901 1.55874 3 0.795609 3 0 
C 3 -0.795609 2.683901 -1.55874 2.12132 -2.12132 
C 1.55874 -2.683901 0.795609 -3 0 -3 
C -0.795609 -3 -1.55874 -2.683901 -2.12132 -2.12132 
C -2.683901 -1.55874 -3 -0.795609 -3 0 
C -3 0.795609 -2.683901 1.55874 -2.12132 2.12132 
C -1.55874 2.683901 -0.795609 3 0 3 
z
" style="stroke: #ff7f0e"/>
    </defs>
    <g clip-path="url(#pd066cb7d0a)">
     <use xlink:href="#m43dc4bf304" x="46.335852" y="131.323263" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="88.808465" y="75.800368" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="144.954206" y="42.543" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="187.426819" y="29.014579" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="254.744317" y="21.404842" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="328.517785" y="18.586421" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="370.990398" y="18.022737" style="fill: #ff7f0e; stroke: #ff7f0e"/>
    </g>
   </g>
   <g id="patch_3">
    <path d="M 30.103125 195.696 
L 30.103125 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 387.223125 195.696 
L 387.223125 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 30.103125 195.696 
L 387.223125 195.696 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 30.103125 7.2 
L 387.223125 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="legend_1">
    <g id="patch_7">
     <path d="M 37.103125 45.201563 
L 128.365625 45.201563 
Q 130.365625 45.201563 130.365625 43.201563 
L 130.365625 14.2 
Q 130.365625 12.2 128.365625 12.2 
L 37.103125 12.2 
Q 35.103125 12.2 35.103125 14.2 
L 35.103125 43.201563 
Q 35.103125 45.201563 37.103125 45.201563 
L 37.103125 45.201563 
z
" style="fill: none; opacity: 0.8; stroke: currentColor; stroke-linejoin: miter"/>
    </g>
    <g id="line2d_31">
     <path d="M 39.103125 20.298438 
L 49.103125 20.298438 
L 59.103125 20.298438 
" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
     <g>
      <use xlink:href="#m98ae7f93d8" x="49.103125" y="20.298438" style="fill: #1f77b4; stroke: #1f77b4"/>
     </g>
    </g>
    <g id="text_11">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="67.103125" y="23.798438" transform="rotate(-0 67.103125 23.798438)">TF-IDF</text>
    </g>
    <g id="line2d_32">
     <path d="M 39.103125 35.299219 
L 49.103125 35.299219 
L 59.103125 35.299219 
" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linecap: square"/>
     <g>
      <use xlink:href="#m43dc4bf304" x="49.103125" y="35.299219" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     </g>
    </g>
    <g id="text_12">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="67.103125" y="38.799219" transform="rotate(-0 67.103125 38.799219)">PPMI + SVD</text>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="pd066cb7d0a">
   <rect x="30.103125" y="7.2" width="357.12" height="188.496"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Etiketli örnek sayısına göre sınav doğruluğu (yatay eksen logaritmik). Ön eğitimli vektörler az etikette çok önde; 300 etikette eşitlik, sonra TF-IDF hafif önde.</figcaption>
</figure>

- 10 etiketle TF-IDF %35, ön eğitimli vektörler %55. 50 etiketle %75'e karşı
  %87. Az etikette ön eğitim büyük fark yaratıyor: TF-IDF yalnızca gördüğü
  kelimeleri tanır; ön eğitimli vektörlerde ise "parcel" zaten "box",
  "arrived" ve yazım hatalı "pracel" ile yakın.
- 300 etikette ikisi eşitleniyor; 1000 ve üstünde TF-IDF biraz öne geçiyor.
  Bol etiket varken her kelimenin ağırlığını doğrudan öğrenmek, 50 sayıya
  sıkıştırılmış ortalamadan daha ince ayrım yapabiliyor.
- Pratik ders: ön eğitim en çok **etiket az olduğunda** kazandırır.
  Gerçek projelerin çoğu bu durumdadır.

## Hiç etiket olmadan

Ön eğitimli vektörlerle hiç etiketli örnek görmeden de sınıflandırma
denenebilir: her kategoriyi bir metinle anlatıp talebi en benzer
anlatıma atamak. Buna **sıfır atışlı** (zero-shot) sınıflandırma denir.

```python
names = ["shipping", "technical", "account", "billing", "refund"]
described = ["parcel delivery", "app error crash", "login password",
             "invoice charge payment", "refund money back"]
for labels in [names, described]:
    C = np.array([embed(text) for text in labels])
    guess = np.array(names)[(D[test] @ C.T).argmax(axis=1)]
    print(round(float(np.mean(guess == y[test])), 3))
```

```text
0.42
0.708
```

- Kategori adlarıyla %42: "shipping", "technical" gibi soyut adlar
  taleplerde pek geçmiyor.
- Kategorileri taleplerin diliyle anlatınca %70,8; tek bir etiketli örnek
  görmeden. Anlatımın sözcükleri sonucu çok değiştiriyor: büyük dil
  modellerine görevi nasıl tarif ettiğinin (istem, prompt) önemli olmasının
  küçük bir örneği.

## Ön eğitimli bir modeli kullanmanın üç yolu

- **Öznitelik çıkarmak** (feature extraction): modelin ürettiği vektörleri
  olduğu gibi alıp üzerine küçük bir sınıflandırıcı eğitmek. Bu bölümde
  yaptığımız. Ucuzdur, az etiketle çalışır.
- **İnce ayar** (fine-tuning): modelin ağırlıklarını da etiketli veriyle
  eğitmeye devam etmek; küçük bir öğrenme oranıyla, ön eğitimin bilgisini
  bozmadan. Bol etiket varsa genellikle en iyi sonucu verir; ama çok az
  etiketle model bildiklerini unutabilir.
- **İstemle kullanmak** (prompting): ağırlıklara hiç dokunmadan görevi
  metinle tarif etmek. Sıfır atışlı denememiz bunun basit bir örneği.

## Özet

- Ön eğitim: bol etiketsiz metinden etiket gerektirmeyen bir görevle dilin
  yapısını öğrenmek. Aktarım: bu bilgiyi az etiketli göreve taşımak.
- 10–50 etiketle ön eğitimli vektörler TF-IDF'i 12–20 puan geçti; 300
  etikette eşitlendiler, binlerce etikette TF-IDF hafif önde.
- Hiç etiket olmadan, kategorileri iyi anlatarak %70,8 doğruluk alındı.
- Ön eğitimli bir model öznitelik çıkarmak, ince ayar ve istemle
  kullanılabilir.
