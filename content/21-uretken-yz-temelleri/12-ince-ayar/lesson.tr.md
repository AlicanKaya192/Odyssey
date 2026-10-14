# İnce Ayar ve Hizalama

Büyük bir dil modeli önce çok büyük bir metinle **ön eğitimden** geçer
(NLP patikasının Önceden Eğitilmiş Modeller bölümü); sıradaki token'ı
tahmin etmeyi öğrenir. Bir sohbet asistanı olması için iki adım daha
gerekir: **talimatla ince ayar** (instruction tuning) ve **tercihle
hizalama** (preference alignment). Bu bölüm ikisinin altındaki fikirleri
küçük NumPy deneyleriyle ölçüyor: ince ayar nedir, neyi bozar ve bir
model "insanların tercih ettiği" cevaplara nasıl yönlendirilir.

## İnce ayar: eğitime kaldığı yerden devam

**İnce ayar** (fine-tuning), önceden eğitilmiş bir modelin ağırlıklarını
yeni bir görevin verisiyle biraz daha eğitmektir. Küçük bir deney
kuralım: 64 → 32 → 10 boyutlu bir ağı 8×8 rakamların yalnızca **0–4**
olanlarıyla eğitiyoruz (bu ağ "ön eğitimli model"). Sonra yeni görev
geliyor: **5–9** rakamlarını tanımak, ama her rakamdan yalnızca 10 örnek
var.

```python
import numpy as np
from gen_data import load_digit_images

X, y = load_digit_images()
y = np.array(y)
order = np.random.default_rng(0).permutation(len(X))
X, y = X[order], y[order]
X_old, y_old = X[y < 5], y[y < 5]
X_new, y_new = X[y >= 5], y[y >= 5]


def init(sizes, rng):
    return [(rng.normal(0, np.sqrt(1 / a), (a, b)), np.zeros(b))
            for a, b in zip(sizes, sizes[1:])]


def forward(x, net):
    acts = [x]
    for i, (W, b) in enumerate(net):
        z = acts[-1] @ W + b
        if i < len(net) - 1:
            acts.append(np.tanh(z))
        else:
            e = np.exp(z - z.max(axis=1, keepdims=True))
            acts.append(e / e.sum(axis=1, keepdims=True))
    return acts


def train(net, X, y, steps, lr=0.5, layers=None):
    net = [(W.copy(), b.copy()) for W, b in net]
    layers = range(len(net)) if layers is None else layers
    onehot = np.eye(10)[y]
    for _ in range(steps):
        acts = forward(X, net)
        grad = (acts[-1] - onehot) / len(X)
        for i in reversed(range(len(net))):
            W, b = net[i]
            gW, gb = acts[i].T @ grad, grad.sum(axis=0)
            if i:
                grad = grad @ W.T * (1 - acts[i] ** 2)
            if i in layers:
                net[i] = (W - lr * gW, b - lr * gb)
    return net


def accuracy(net, X, y):
    return round(float((forward(X, net)[-1].argmax(1) == y).mean()), 3)


pre = train(init([64, 32, 10], np.random.default_rng(0)),
            X_old[:700], y_old[:700], 500)
print("old task", accuracy(pre, X_old[700:], y_old[700:]))
```

```text
old task 1.0
```

Ön eğitimli ağ eski görevde (0–4) neredeyse kusursuz. Şimdi yeni görevin
50 örneğiyle iki biçimde ince ayar yapalım: **bütün ağırlıkları**
güncelleyerek ve yalnızca **son katmanı** güncelleyerek (alttaki katman
dondurulmuş).

```python
few = np.concatenate([np.where(y_new[:400] == d)[0][:10]
                      for d in range(5, 10)])
Xf, yf = X_new[few], y_new[few]
full = train(pre, Xf, yf, 300)
head = train(pre, Xf, yf, 300, layers=[1])
for name, net in [("full", full), ("last layer", head)]:
    print(f"{name:10} new task {accuracy(net, X_new[400:], y_new[400:])}",
          f"old task {accuracy(net, X_old[700:], y_old[700:])}")
```

```text
full       new task 0.931 old task 0.065
last layer new task 0.802 old task 0.189
```

Bütün ağırlıklarla ince ayar yeni görevde %93'e ulaştı; yalnızca son
katman %80'de kaldı: 0–4 için öğrenilen ara özellikler 5–9'u ayırmaya
tam yetmiyor. Ama bedeli büyük: ince ayardan sonra ağ eski görevde
%6,5'e düştü, 0–4 rakamlarının neredeyse hiçbirini tanımıyor. Buna
**felaket düzeyinde unutma** (catastrophic forgetting) denir: yeni veride
eskiye dair hiçbir örnek olmadığı için model eskiyi korumak zorunda
kalmıyor. Yalnızca son katmanı eğitmek de unutturuyor (%19), çünkü çıkış
katmanı artık yalnızca 5–9 cevabını vermeyi öğreniyor.

## Unutmanın çaresi: eskiyi de karıştır

İnce ayar verisine eski görevden birkaç örnek karıştırmak (**tekrar**,
replay) modelin eskiyi de korumasını sağlar. Aynı deneyi üç tohumla, 50
yeni örneğe 50 eski örnek katarak tekrarlayalım:

```python
for seed in [0, 1, 2]:
    rng = np.random.default_rng(seed)
    base = train(init([64, 32, 10], rng), X_old[:700], y_old[:700], 500)
    replay = rng.choice(700, 50, replace=False)
    Xm = np.concatenate([Xf, X_old[replay]])
    ym = np.concatenate([yf, y_old[replay]])
    only_new, mixed = train(base, Xf, yf, 300), train(base, Xm, ym, 300)
    print(seed, "only new:", accuracy(only_new, X_new[400:], y_new[400:]),
          accuracy(only_new, X_old[700:], y_old[700:]),
          "| mixed:", accuracy(mixed, X_new[400:], y_new[400:]),
          accuracy(mixed, X_old[700:], y_old[700:]))
```

```text
0 only new: 0.931 0.065 | mixed: 0.901 0.95
1 only new: 0.938 0.055 | mixed: 0.893 0.98
2 only new: 0.921 0.045 | mixed: 0.865 0.945
```

Yalnızca yeni veriyle ince ayarda eski görevin doğruluğu üç tohumda da
%4,5–6,5. 50 eski örnek karıştırınca %94,5–98'de kalıyor. Bedeli yeni
görevde birkaç puan (%92–94'ten %86,5–90'a): ağın kapasitesi artık iki
görev arasında paylaşılıyor.

## Talimatla ince ayar

Ön eğitimli bir dil modeli metni devam ettirir ama "soruyu cevapla" diye
bir görev bilmez. **Talimatla ince ayar**, modeli binlerce (talimat, iyi
cevap) çiftiyle eğitmektir:

```text
{"instruction": "Summarise the return policy in one sentence.",
 "response": "You can return unused items within 30 days of delivery."}
{"instruction": "Is shipping free for a 30 euro order?",
 "response": "No. Shipping is free only over 50 euros."}
```

Model bu verideki biçimi öğrenir: talimata cevap vermek, istenen
uzunlukta yazmak, kaynakta yoksa söylemek. Yukarıdaki deneyin dersi burada
da geçerli: yalnızca yeni veriyle eğitmek modelin eski becerilerini
aşındırabilir; bu yüzden ince ayar verisine genel amaçlı örnekler de
karıştırılır.

## Tercihten ödül modeli

Bir cevabın "iyi" olduğunu yazmak zordur, ama iki cevaptan hangisinin
daha iyi olduğunu söylemek kolaydır. **Tercihle hizalama** bu yüzden ikili
karşılaştırmalardan öğrenir. Önce bir **ödül modeli** (reward model)
kurulur: her cevaba bir puan $r$ verir ve "a, b'ye tercih edilir"
olasılığı $\sigma(r(a) - r(b))$ olur (Bradley–Terry modeli).

Bunu yapay bir veriyle görelim. Her cevabı üç özellikle anlatıyoruz:
doğru mu (0/1), kaynak gösteriyor mu (0/1), uzunluğu (0,2–2,0). Etiketçi
gibi davranan bir kural, gizli ağırlıklarla (`TRUE_W`: doğruluk 3, kaynak
1, uzunluk −0,5) ve biraz rastlantıyla 400 çiftte tercih yapıyor. Ödül
modelini yalnızca bu tercihlerden öğreniyoruz:

```python
def features(rng, n):
    return np.column_stack([rng.integers(0, 2, n), rng.integers(0, 2, n),
                            rng.uniform(0.2, 2.0, n)])


def preferences(F, weights, rng, n_pairs=400):
    pairs = rng.integers(0, len(F), (n_pairs, 2))
    pairs = pairs[pairs[:, 0] != pairs[:, 1]]
    diff = F[pairs[:, 0]] - F[pairs[:, 1]]
    first = rng.random(len(pairs)) < 1 / (1 + np.exp(-diff @ weights))
    return np.where(first[:, None], diff, -diff)


def fit_reward(D, steps=2000, lr=0.5):
    w = np.zeros(D.shape[1])
    for _ in range(steps):
        p = 1 / (1 + np.exp(-D @ w))
        w += lr * D.T @ (1 - p) / len(D)
    return w


rng = np.random.default_rng(0)
TRUE_W = np.array([3.0, 1.0, -0.5])
answers = features(rng, 300)
w = fit_reward(preferences(answers, TRUE_W, rng))
print("learned", w.round(2), "hidden", TRUE_W)
```

```text
learned [ 2.63  1.31 -0.72] hidden [ 3.   1.  -0.5]
```

`preferences` her çifti "tercih edilen − tercih edilmeyen" özellik farkı
olarak döndürüyor; `fit_reward` bu farkların olasılığını büyüten
ağırlıkları gradyan çıkışıyla buluyor (lojistik regresyon). Öğrenilen
ağırlıklar gizlilere yakın: model, etiketçinin neyi ödüllendirdiğini
yalnızca tercihlerden çıkardı.

## Ödülle seçmek

Ödül modeli olunca en basit kullanım: aynı soruya birkaç cevap üret,
ödülü en yüksek olanı seç (**en iyi n**, best-of-n). Gerçek hizalama
yöntemleri (pekiştirmeli öğrenme ya da doğrudan tercih eğitimi) modeli
ödülü yüksek cevaplar üretmeye doğru eğitir; fikir aynı.

```python
candidates = features(rng, 8000).reshape(1000, 8, 3)
best = candidates[np.arange(1000), (candidates @ w).argmax(axis=1)]
print("correct: first answer", candidates[:, 0, 0].mean().round(3),
      "best of 8", best[:, 0].mean().round(3))
```

```text
correct: first answer 0.497 best of 8 0.993
```

İlk cevabın doğru olma oranı %50 (rastgele); ödül modeliyle 8 cevaptan
seçince %99. Modelin kendisi değişmedi, yalnızca seçerek cevaplar
iyileşti. Bedeli 8 kat üretim.

## Ödülü kandırmak

Ödül modeli etiketçilerin tercihlerini öğrenir; **hatalarını da**.
Etiketçiler doğruluğu denetlemekte zorlanıp uzun, ayrıntılı görünen
cevapları seviyorsa (gizli ağırlıklar: doğruluk 0,5, kaynak 0,2, uzunluk
1,5) ne olur?

```python
BIASED_W = np.array([0.5, 0.2, 1.5])
w_biased = fit_reward(preferences(answers, BIASED_W, rng))
picked = candidates[np.arange(1000), (candidates @ w_biased).argmax(axis=1)]
print("learned", w_biased.round(2))
print("best of 8: correct", picked[:, 0].mean().round(3),
      "length", picked[:, 2].mean().round(2),
      "| first answer length", candidates[:, 0, 2].mean().round(2))
```

```text
learned [0.56 0.31 1.6 ]
best of 8: correct 0.776 length 1.75 | first answer length 1.09
```

Ödül modeli etiketçilerin yanlılığını sadakatle öğrendi: uzunluğun
ağırlığı 1,6. Ödülle seçilen cevaplar ortalama 1,75 uzunlukta (ilk
cevaplarda 1,09) ve doğru oranı %78: rastgeleden iyi, ama doğru ödülle
seçilen %99'un çok altında. Ödülü en yükseğe çıkarmak, ödülün ölçtüğü şeyi
(uzunluk) artırdı, istenen şeyi (doğruluk) değil. Buna **ödülü kandırma**
(reward hacking) denir. Gereksiz uzun, kendinden emin görünen cevaplar
gerçek modellerde de sık bildirilen bir örneği; bu yüzden tercih verisi
dikkatle toplanır ve hizalanan model ayrıca, ödülden bağımsız ölçülerle
değerlendirilir.

## Özet

- İnce ayar: önceden eğitilmiş modeli yeni veriyle eğitmeye devam etmek;
  bütün ağırlıklar ya da yalnızca bir kısmı güncellenir.
- Yalnızca yeni veriyle ince ayar eski görevi unutturabilir (bölümde
  doğruluk ~1,0'dan ~0,05'e); eski verinin bir kısmını karıştırmak bunu
  büyük ölçüde önledi.
- Talimatla ince ayar, (talimat, iyi cevap) çiftleriyle modele "soruya
  cevap vermeyi" öğretir.
- Tercihle hizalama, ikili karşılaştırmalardan bir ödül modeli öğrenip
  modeli ödülü yüksek cevaplara yöneltir.
- Ödül modeli etiketçilerin yanlılıklarını da öğrenir; ödülü yükseltmek
  her zaman cevabı iyileştirmez.
