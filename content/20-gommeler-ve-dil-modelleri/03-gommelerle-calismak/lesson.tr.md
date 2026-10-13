# Gömmelerle Çalışmak

Kelime vektörlerini iki yoldan kurmayı öğrendik. Bu bölüm onları
**kullanmak** üzerine: bir dosyaya yazıp okumak, dağarcıkta olmayan
kelimeyle karşılaşmak, en yakın komşuları hızlı bulmak. Sonra gömmelerin
en önemli tuzağına bakacağız: **önyargı** (bias). Gömmeler eğitildikleri
metnin kalıplarını öğrenir; metin "hemşire" deyince hep "she" diyorsa,
vektör de bunu taşır. Bu önyargıyı ölçecek, silmeye çalışacak ve silmenin
neden kolay olmadığını göreceğiz.

Bu bölümde külliyata meslekler üzerine 4000 cümle (`make_jobs`)
ekliyoruz. Bu cümleler bilerek önyargılı: "nurse" cümlelerinin %85'inde
zamir "she", "engineer" cümlelerinin %85'inde "he". Önyargıyı açıkça
yakalamak için pencereyi 3, boyutu 50 seçtik.

## Vektörleri kaydetmek ve okumak

Eğitilmiş gömmeler genellikle düz metin olarak paylaşılır: her satırda kelime
ve sayıları. Gerçek hazır gömme dosyaları da çoğunlukla bu biçimdedir.

```python
import numpy as np
from corpus_data import JOB_SKEW, GENDER_PAIRS, make_corpus, make_jobs

sentences = [s.split() for s in make_corpus(20000) + make_jobs(4000)]
vocab = sorted({w for s in sentences for w in s})
index = {w: i for i, w in enumerate(vocab)}
M = np.zeros((len(vocab), len(vocab)))
for s in sentences:
    for i, w in enumerate(s):
        for j in range(max(0, i - 3), min(len(s), i + 4)):
            if j != i:
                M[index[w], index[s[j]]] += 1
with np.errstate(divide="ignore"):
    P = np.maximum(np.log(M * M.sum() / np.outer(M.sum(1), M.sum(0))), 0)
U, S, _ = np.linalg.svd(P)
E = U[:, :50] * S[:50]
E = E / np.linalg.norm(E, axis=1, keepdims=True)

with open("vectors.txt", "w", encoding="utf-8") as f:
    for word in vocab:
        f.write(word + " " + " ".join(f"{x:.4f}" for x in E[index[word]]) + "\n")
loaded = {}
with open("vectors.txt", encoding="utf-8") as f:
    for line in f:
        word, *numbers = line.split()
        loaded[word] = np.array(numbers, dtype=float)
print(len(loaded), len(loaded["cat"]))
print(round(float(np.abs(loaded["cat"] - E[index["cat"]]).max()), 5))
```

```text
185 50
5e-05
```

- 185 kelime, her biri 50 sayı. Dört basamağa yuvarladığımız için okunan
  vektör aslından en fazla 0,00005 farklı; benzerlik hesapları için önemsiz.
- `word, *numbers = line.split()` satırın ilk parçasını kelimeye, gerisini
  listeye alıyor.
- Büyük gömme dosyalarında (yüz binlerce kelime × 300 sayı) metin biçimi
  yavaş okunur; o zaman `np.save` ile ikili biçim ve ayrı bir kelime
  listesi kullanılır.

## Dağarcıkta olmayan kelime

Gömme tablosu yalnızca eğitimde görülen kelimeleri bilir. Yeni bir kelime
gelince bir karar vermek gerekir:

```python
def vector(word):
    return loaded.get(word)


sentence = "the cat ate pizza".split()
known = [w for w in sentence if vector(w) is not None]
print(known, [w for w in sentence if w not in known])
average = np.mean([vector(w) for w in known], axis=0)
print(average.shape)
```

```text
['the', 'cat', 'ate'] ['pizza']
(50,)
```

- "pizza" eğitimde hiç geçmedi: vektörü yok. Burada onu atlayıp bilinen
  kelimelerin ortalamasını aldık (bir sonraki bölümün konusu: belge
  vektörü).
- Diğer seçenekler: sıfır vektörü vermek, ya da bir "bilinmeyen" (UNK)
  vektörü öğrenmek. Kalıcı çözüm alt kelime parçalarıdır: "pizza"
  bilinmese de "piz" ve "za" bilinebilir. Bunu BPE bölümünde göreceğiz.

## En yakın komşuları hızlı bulmak

Komşu bulmak için bütün benzerlikleri hesaplayıp sıralıyorduk. Yalnızca ilk
k gerekiyorsa her şeyi sıralamak gereksiz: `np.argpartition` k en büyüğü
sırasız ama doğrusal zamanda bulur, sonra yalnızca o k tanesi sıralanır.

```python
sims = E @ E[index["cat"]]
top = np.argpartition(-sims, 5)[:5]
top = top[np.argsort(-sims[top])]
print([vocab[i] for i in top])
print([vocab[i] for i in np.argsort(-sims)[:5]])
```

```text
['cat', 'cow', 'mouse', 'horse', 'rabbit']
['cat', 'cow', 'mouse', 'horse', 'rabbit']
```

İki yol aynı sonucu veriyor (ilk sırada "cat"in kendisi). 185 kelimede fark
hissedilmez; bir milyon kelimelik bir gömme tablosunda bütün diziyi
sıralamak yerine k tanesini bulmak belirgin biçimde hızlıdır. Çok büyük
tablolarda yaklaşık en yakın komşu (ANN) yöntemleri kullanılır; 13.
bölümde gördüğün LSH bunlardan biri.

## Önyargıyı ölçmek

Cinsiyet ilişkisini taşıyan bir **yön** bulalım: kadın ve erkek kelime
çiftlerinin farklarının ortalaması ("woman − man", "queen − king", "she −
he"...). Bir kelimenin bu yöne izdüşümü (nokta çarpım) ne kadar "kadın" ya
da "erkek" tarafta durduğunu söyler.

```python
pairs = GENDER_PAIRS + [("he", "she"), ("his", "her")]
gender = np.mean([E[index[f]] - E[index[m]] for m, f in pairs], axis=0)
gender = gender / np.linalg.norm(gender)
jobs = list(JOB_SKEW)
projection = np.array([E[index[j]] @ gender for j in jobs])
for job, p in zip(jobs, projection):
    print(f"{job:<10} {JOB_SKEW[job]:.2f} {p:+.3f}")
skew = np.array([JOB_SKEW[j] for j in jobs])
print(round(float(np.corrcoef(projection, skew)[0, 1]), 3))
```

```text
nurse      0.85 +0.167
secretary  0.85 +0.137
dancer     0.80 +0.131
florist    0.80 +0.151
engineer   0.15 -0.227
pilot      0.15 -0.229
mechanic   0.20 -0.231
plumber    0.20 -0.217
teacher    0.50 -0.046
writer     0.50 -0.055
0.997
```

- Verideki "she" oranı yüksek olan meslekler pozitif, düşük olanlar negatif
  tarafta; yarı yarıya olanlar (teacher, writer) ortaya yakın.
- Korelasyon 0,997: vektörler verideki önyargıyı neredeyse birebir
  kopyalamış. Model "hemşirelik kadın işidir" diye bir şey öğrenmeye
  çalışmadı; yalnızca hangi kelimelerin birlikte geçtiğini saydı.

## Önyargılı benzetmeler

Benzetmeyi yalnızca meslekler arasında soralım:

```python
def analogy(E, a, b, c, candidates):
    sims = E @ (E[index[b]] - E[index[a]] + E[index[c]])
    return max(candidates, key=lambda w: -np.inf if w in (a, b, c) else sims[index[w]])


print(analogy(E, "man", "engineer", "woman", jobs))
print(analogy(E, "he", "pilot", "she", jobs))
print(analogy(E, "she", "nurse", "he", jobs))
```

```text
florist
engineer
secretary
```

"man : engineer :: woman : ?" sorusuna cevap "florist". Gerçek gömmelerde de
benzer sonuçlar yayımlandı (Bolukbasi ve arkadaşları, 2016: "man : computer
programmer :: woman : homemaker"). Böyle vektörlerle kurulan bir sistem,
örneğin özgeçmiş sıralayan bir arama, önyargıyı karara taşıyabilir.

Öteki iki soruda cevaplar "engineer" ve "secretary": benzetme hesabı çoğu
zaman sorudaki kelimenin ("pilot", "nurse") en yakın komşusuna kayar. Bu,
benzetme testinin bilinen bir zayıflığıdır; tek bir benzetmeye bakarak
karar verme.

## Önyargıyı silmeye çalışmak

En bilinen yöntem **nötrleştirmek** (neutralize): cinsiyetle ilgisi
olmaması gereken kelimelerin vektöründen cinsiyet yönündeki bileşeni
çıkarmak.

```python
D = E.copy()
for job in jobs:
    v = D[index[job]] - (D[index[job]] @ gender) * gender
    D[index[job]] = v / np.linalg.norm(v)
print(round(float(max(abs(D[index[j]] @ gender) for j in jobs)), 6))
print(analogy(D, "man", "engineer", "woman", jobs))


def job_neighbours(E, word):
    sims = {j: E[index[word]] @ E[index[j]] for j in jobs if j != word}
    return sorted(sims, key=sims.get, reverse=True)[:3]


print(job_neighbours(E, "nurse"), job_neighbours(D, "nurse"))
```

```text
0.0
florist
['secretary', 'dancer', 'florist'] ['secretary', 'dancer', 'florist']
```

- İzdüşüm artık sıfır: ölçtüğümüz önyargı "silindi".
- Ama benzetme hâlâ "florist" ve "nurse"ün en yakın meslekleri hâlâ öteki
  "kadın" meslekleri. Önyargı tek bir yönde değil; mesleklerin
  birbirine göre dizilişinde de var. Gonen ve Goldberg (2019) bunu gerçek
  gömmelerde gösterdi ve bu tür silmeyi "domuza ruj sürmek" diye
  adlandırdı.
- Ders: önyargıyı tek bir ölçüyle sıfırlamak onu yok etmez. Gömmelerle
  karar veren bir sistemde önyargı, sistemin **kararları** üzerinde
  ölçülmeli; verinin kendisi de gözden geçirilmeli.

## Özet

- Gömmeler satır başına "kelime sayılar" biçiminde saklanır; büyük
  tablolarda ikili biçim.
- Dağarcıkta olmayan kelimeye bir karar gerekir: atla, sıfır ver, UNK
  vektörü ya da alt kelime parçaları.
- İlk k komşu için `np.argpartition` bütün sıralamadan hızlıdır.
- Gömmeler verideki önyargıyı taşır: projeksiyon ile veri oranı arasında
  0,997 korelasyon. Nötrleştirmek ölçüyü sıfırlar ama benzetmeleri ve
  komşulukları düzeltmez.
