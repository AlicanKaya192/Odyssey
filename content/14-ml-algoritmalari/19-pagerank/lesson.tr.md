# PageRank

Bir web sayfası ne kadar önemli? İlk akla gelen, ona kaç sayfanın bağlantı
verdiğini saymak. **PageRank** daha ince bir soru sorar: önemli sayfalardan
gelen bağlantı daha değerlidir. Google'ın ilk arama motorunun temelindeki bu
fikir, bugün sosyal ağlarda etkili kişiyi, atıf ağlarında önemli makaleyi,
yol ağlarında kritik kavşağı bulmakta da kullanılıyor. Bu bölümde PageRank'i
**kuvvet yinelemesiyle** (power iteration) sıfırdan yazıp doğrusal denklemin
tam çözümüyle karşılaştırıyoruz.

## Rastgele gezgin

Bir gezgin düşün: her adımda bulunduğu sayfanın bağlantılarından birine
rastgele tıklıyor. Ara sıra da (olasılık `1 − d`) sıkılıp rastgele bir
sayfaya atlıyor. Uzun süre gezdikten sonra hangi sayfada bulunma olasılığı
ne? O olasılık sayfanın **PageRank**'idir. `d`'ye **sönümleme** (damping)
katsayısı denir; klasik değeri 0,85.

Bunu bir matrisle yazarız: `M[i, j]`, `j` sayfasından `i` sayfasına geçme
olasılığı (`j`'nin her bağlantısına eşit pay). Bir adımda olasılıklar
`r → d · M r + (1 − d) / n` diye güncellenir; bunu değişim duruncaya kadar
tekrarlamak **kuvvet yinelemesidir**.

```python
import numpy as np

pages = ["A", "B", "C", "D", "E", "F"]
links = {"A": ["B", "C"], "B": ["C"], "C": ["A"],
         "D": ["C", "E"], "E": ["C", "F"], "F": ["C"]}
n = len(pages)
idx = {p: i for i, p in enumerate(pages)}


def transition(links):
    M = np.zeros((n, n))                 # M[i, j]: j'den i'ye geçme olasılığı
    for p, outs in links.items():
        for q in outs:
            M[idx[q], idx[p]] = 1 / len(outs)
    return M


def pagerank(M, d=0.85, tol=1e-10):
    r = np.full(n, 1 / n)                # herkes eşit başlar
    for it in range(1, 1000):
        new = d * M @ r + (1 - d) / n
        if np.abs(new - r).sum() < tol:
            return new, it
        r = new
    return r, it


def show(r):
    return " ".join(f"{p}={v:.3f}" for p, v in zip(pages, r))


M = transition(links)
r, it = pagerank(M)
print(show(r))
print(it, round(r.sum(), 6))
exact = np.linalg.solve(np.eye(n) - 0.85 * M, np.full(n, 0.15 / n))
print(np.abs(exact - r).max() < 1e-9)
print({p: sum(p in outs for outs in links.values()) for p in pages})
```

```text
A=0.347 B=0.173 C=0.379 D=0.025 E=0.036 F=0.040
46 1.0
True
{'A': 1, 'B': 1, 'C': 5, 'D': 0, 'E': 1, 'F': 1}
```

Yineleme 46 adımda durdu ve olasılıkların toplamı 1. Aynı sonuç doğrusal
denklemin tam çözümünden de çıkıyor: `(I − d M) r = (1 − d) / n`. En çok
bağlantı alan C (5 bağlantı) birinci, 0,379. Asıl ilginç olan A: yalnızca
**bir** bağlantısı var ama 0,347 ile ikinci. Çünkü o tek bağlantı C'den
geliyor ve C bütün değerini yalnızca A'ya veriyor. B, E ve F'ye de birer
bağlantı geliyor, ama önemsiz sayfalardan.
PageRank bağlantıları saymaz, **tartar**.

<figure class="fig">
<svg viewBox="0 0 520 330" width="520" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arr19" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="dim" d="M0 0L10 5L0 10z"/></marker></defs><line class="line" x1="174.5" y1="68.3" x2="352.1" y2="61.5" marker-end="url(#arr19)"/><line class="line" x1="164.8" y1="98.4" x2="215.1" y2="129.4" marker-end="url(#arr19)"/><line class="line" x1="361.2" y1="79.9" x2="300.3" y2="122.1" marker-end="url(#arr19)"/><line class="line" x1="224.0" y1="120.8" x2="173.6" y2="89.8" marker-end="url(#arr19)"/><line class="line" x1="107.9" y1="239.5" x2="217.8" y2="174.8" marker-end="url(#arr19)"/><line class="line" x1="110.4" y1="253.6" x2="234.9" y2="275.6" marker-end="url(#arr19)"/><line class="line" x1="260.0" y1="257.5" x2="260.0" y2="199.0" marker-end="url(#arr19)"/><line class="line" x1="281.8" y1="274.5" x2="394.7" y2="246.3" marker-end="url(#arr19)"/><line class="line" x1="399.9" y1="228.7" x2="302.7" y2="174.0" marker-end="url(#arr19)"/><circle class="box" cx="130" cy="70" r="44.5"/><circle class="curve" cx="130" cy="70" r="44.5"/><text class="ink" x="130" y="69" font-size="14" text-anchor="middle">A</text><text class="dim" x="130" y="83" font-size="10" text-anchor="middle">0.347</text><circle class="box" cx="390" cy="60" r="35.0"/><circle class="curve" cx="390" cy="60" r="35.0"/><text class="ink" x="390" y="59" font-size="14" text-anchor="middle">B</text><text class="dim" x="390" y="73" font-size="10" text-anchor="middle">0.173</text><circle class="box" cx="260" cy="150" r="46.0"/><circle class="curve" cx="260" cy="150" r="46.0"/><text class="ink" x="260" y="149" font-size="14" text-anchor="middle">C</text><text class="dim" x="260" y="163" font-size="10" text-anchor="middle">0.379</text><circle class="box" cx="90" cy="250" r="20.7"/><circle class="curve" cx="90" cy="250" r="20.7"/><text class="ink" x="90" y="249" font-size="14" text-anchor="middle">D</text><text class="dim" x="90" y="263" font-size="10" text-anchor="middle">0.025</text><circle class="box" cx="260" cy="280" r="22.5"/><circle class="curve" cx="260" cy="280" r="22.5"/><text class="ink" x="260" y="279" font-size="14" text-anchor="middle">E</text><text class="dim" x="260" y="293" font-size="10" text-anchor="middle">0.036</text><circle class="box" cx="420" cy="240" r="23.0"/><circle class="curve" cx="420" cy="240" r="23.0"/><text class="ink" x="420" y="239" font-size="14" text-anchor="middle">F</text><text class="dim" x="420" y="253" font-size="10" text-anchor="middle">0.040</text></svg>
<figcaption>Altı sayfalık ağ; oklar bağlantılar, dairenin büyüklüğü PageRank. A'ya tek bir ok geliyor ama o ok, bütün değerini A'ya veren C'den.</figcaption>
</figure>

## Çıkışı olmayan sayfa

Hiçbir yere bağlantı vermeyen bir sayfa (**çıkmaz**, dangling node) gezgini
yutar: `M`'nin o sütunu sıfırdır ve olasılık her adımda sızar. F'nin
bağlantısını silelim:

```python
links2 = dict(links, F=[])
M2 = transition(links2)
r2, _ = pagerank(M2)
print(show(r2), round(r2.sum(), 3))
M2[:, idx["F"]] = 1 / n                  # çıkmazdan her sayfaya eşit
r3, _ = pagerank(M2)
print(show(r3), round(r3.sum(), 3))
```

```text
A=0.260 B=0.135 C=0.276 D=0.025 E=0.036 F=0.040 0.773
A=0.336 B=0.175 C=0.358 D=0.032 E=0.046 F=0.052 1.0
```

Düzeltmeden önce toplam 0,773: olasılığın beşte birinden fazlası F'de
kayboldu. Yaygın çare, çıkmaz sayfadan bütün sayfalara eşit bağlantı varmış
gibi davranmak; toplam yeniden 1.

## Sönümleme katsayısı

```python
for d in (0.5, 0.85, 0.99):
    rd, steps = pagerank(M, d)
    print(d, show(rd), steps)
```

```text
0.5 A=0.242 B=0.144 C=0.317 D=0.083 E=0.104 F=0.109 23
0.85 A=0.347 B=0.173 C=0.379 D=0.025 E=0.036 F=0.040 46
0.99 A=0.396 B=0.198 C=0.399 D=0.002 E=0.002 F=0.003 65
```

`d` küçükse gezgin sık sık rastgele atlar: sıralar birbirine yaklaşır
(D bile 0,083) ve yineleme hızlı (23 adım). `d` 1'e yaklaşınca bağlantılar
belirleyici olur: A, B ve C kendi aralarında kapalı bir döngü kuruyor (oradan
dışarı bağlantı yok) ve 0,99'da olasılığın neredeyse hepsini topluyor; D, E,
F sıfıra iniyor ve yineleme 65 adım sürüyor. 0,85 bu iki uç arasında bir
denge.

## Büyük ağda yakınsama

1000 sayfalık rastgele bir ağda (her sayfa 1–10 bağlantı) hatanın nasıl
küçüldüğüne bakalım:

```python
rng = np.random.default_rng(19)
N = 1000
Mb = np.zeros((N, N))
for j in range(N):
    k = rng.integers(1, 11)
    Mb[rng.choice(N, k, replace=False), j] = 1 / k
exact_b = np.linalg.solve(np.eye(N) - 0.85 * Mb, np.full(N, 0.15 / N))
rb = np.full(N, 1 / N)
for it in range(1, 41):
    rb = 0.85 * Mb @ rb + 0.15 / N
    if it % 10 == 0:
        print(it, f"{np.abs(rb - exact_b).sum():.1e}")
```

```text
10 1.1e-04
20 7.3e-08
30 6.8e-11
40 6.6e-14
```

Hata her 10 adımda yaklaşık bin kat küçülüyor; 40 adımda
6,6 × 10⁻¹⁴. Teorik garanti daha gevşek: hata her adımda en az `d` katına
iner (10 adımda `0,85¹⁰ ≈ 0,197`). Gerçek web'de milyarlarca sayfa olduğu
için tam çözüm (matris tersi) imkânsız; kuvvet yinelemesi yalnızca matris
çarpımı ister ve birkaç düzine adımda yeter.

## Özet

- PageRank, rastgele gezginin uzun vadede bir sayfada bulunma olasılığı.
- `r ← d M r + (1 − d)/n`; değişim duruncaya kadar tekrar (kuvvet
  yinelemesi). Tam çözüm `(I − d M) r = (1 − d)/n` ile aynı.
- Bağlantılar sayılmaz, tartılır: önemli sayfadan gelen bağlantı değerlidir.
- Çıkmaz sayfalar olasılığı sızdırır; onlardan her sayfaya eşit geçiş
  varsayılır.
- `d` küçükse sıralar düzleşir; 1'e yakınsa kapalı döngüler her şeyi toplar.
