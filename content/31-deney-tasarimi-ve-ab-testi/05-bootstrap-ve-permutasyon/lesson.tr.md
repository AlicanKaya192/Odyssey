# Bootstrap ve Permütasyon Testi

Şimdiye kadar her soru için bir formül vardı: oranlar için z-testi,
ortalamalar için Welch. Ama her istatistiğin hazır formülü yoktur: iki
grubun **medyan** farkı, bir yüzdelik, iki toplamın oranı. Bu bölüm
formül yerine bilgisayarın gücünü kullanan iki yöntemi gösteriyor:
güven aralığı için **bootstrap**, hipotez testi için **permütasyon
testi**.

## Bootstrap: örneklemden yeniden örneklemek

Örneklem ve Evren bölümünde, aynı evrenden binlerce örneklem çekip
tahminin nasıl oynadığını görmüştük. Gerçek hayatta evren elimizde yok;
yalnızca bir örneklem var. **Bootstrap** fikri şu: örneklemin kendisini
evren yerine koy, ondan **yerine koyarak** (aynı satır birden çok kez
seçilebilir) aynı büyüklükte yeni örneklemler çek ve istatistiği her
birinde hesapla. Bu değerlerin dağılımı, tahminin ne kadar oynadığını
gösterir.

İlk A/B Testinin Çözümlemesi bölümündeki gelir farkı için:

```python
import numpy as np
from scipy import stats
from ab_data import make_experiment

test = make_experiment()
rev_a = test.loc[test["group"] == "A", "revenue"].to_numpy()
rev_b = test.loc[test["group"] == "B", "revenue"].to_numpy()
rng = np.random.default_rng(501)
diffs = []
for _ in range(2000):
    sample_a = rng.choice(rev_a, size=len(rev_a))
    sample_b = rng.choice(rev_b, size=len(rev_b))
    diffs.append(sample_b.mean() - sample_a.mean())
low, high = np.percentile(diffs, [2.5, 97.5])
print(round(low, 2), round(high, 2))
se = np.sqrt(rev_a.var(ddof=1) / len(rev_a) + rev_b.var(ddof=1) / len(rev_b))
diff = rev_b.mean() - rev_a.mean()
print(round(diff - 1.96 * se, 2), round(diff + 1.96 * se, 2))
```

```text
-1.02 1.41
-0.98 1.38
```

İlk satır bootstrap'in **yüzdelik aralığı** (2000 farkın ortadaki %95'i),
ikinci satır Welch formülünün aralığı. İkisi neredeyse aynı: 15 000'er
kişide merkezi limit teoremi işliyor ve formül doğru. Bootstrap'in asıl işe
yaradığı yer formülün olmadığı yer.

## Formülü olmayan bir istatistik: medyan

Değişiklik sipariş tutarını (alıcıların harcadığı) değiştirdi mi? Tutar
çok çarpık, bu yüzden medyana bakmak isteyebiliriz. İki medyanın farkının
basit bir standart hata formülü yok, ama bootstrap'e fark etmez:

```python
order_a = rev_a[rev_a > 0]
order_b = rev_b[rev_b > 0]
med = []
for _ in range(2000):
    med.append(np.median(rng.choice(order_b, size=len(order_b)))
               - np.median(rng.choice(order_a, size=len(order_a))))
print(round(np.median(order_a), 2), round(np.median(order_b), 2))
print(np.round(np.percentile(med, [2.5, 97.5]), 2))
```

```text
71.72 66.47
[-9.48  0.04]
```

Medyan sipariş tutarı B'de 5,25 daha düşük görünüyor, ama
aralık sıfırı içine alıyor: bu fark şansla açıklanabilir. (Veriyi biz
ürettik; gerçekte sipariş tutarı iki grupta aynı dağılımdan geliyor.)
Medyan, ortalamadan çok daha gürültülüdür; aralığın genişliği bunu
gösteriyor.

## Permütasyon testi: etiketleri karıştırmak

H₀ "B'nin hiçbir etkisi yok" der. Bu doğruysa bir kişinin A mı B mi
olduğu etiketi sonucu değiştirmez; etiketleri karıştırınca ortaya çıkan
farklar, H₀ dünyasında görülebilecek farklardır. **Permütasyon testi** bu
karıştırmayı binlerce kez yapar ve gerçek farktan en az o kadar uç
farkların payını sayar: bu pay p değeridir.

```python
labels = (test["group"] == "B").to_numpy()
bought = test["bought"].to_numpy()
observed = bought[labels].mean() - bought[~labels].mean()
count = 0
for _ in range(5000):
    shuffled = rng.permutation(labels)
    diff_perm = bought[shuffled].mean() - bought[~shuffled].mean()
    count += abs(diff_perm) >= abs(observed)
print(round(observed, 4), round(count / 5000, 4))
```

```text
0.0123 0.0016
```

Permütasyon p'si 0,0016; İlk A/B Testinin Çözümlemesi
bölümündeki z-testi 0,0012 vermişti. İki yöntem aynı yerde
buluşuyor. Permütasyon testi hiçbir dağılım varsaymaz: yalnızca rastgele
atamaya dayanır. Bu yüzden A/B testinde özellikle doğaldır: etiketleri
karıştırmak, atamayı yeniden yapmak demektir.

İki not:

- 5000 karıştırmayla en küçük ölçülebilir p kabaca 1/5000'dir. Çok küçük p
  değerleri için daha çok karıştırma gerekir.
- Hipotez Testinin Mantığı bölümünde H₀ dünyasını benzetimle kurmuştuk;
  permütasyon testi aynı fikrin, elimizdeki veriyle yapılmış hâlidir.

## Bootstrap sihir değildir

Küçük ve çok çarpık örneklemde bootstrap da zorlanır. Gerçek ortalaması
bilinen çarpık bir dağılımdan 20'şer gözlemlik 400 örneklem çekelim ve her
birinde iki aralığın gerçek ortalamayı ne sıklıkla yakaladığını sayalım:

```python
rng2 = np.random.default_rng(502)
true_mean = np.exp(4.2 + 0.9 ** 2 / 2)
hits_t = hits_boot = 0
for _ in range(400):
    x = rng2.lognormal(4.2, 0.9, 20)
    se_x = x.std(ddof=1) / np.sqrt(20)
    low, high = stats.t.interval(0.95, 19, loc=x.mean(), scale=se_x)
    hits_t += low <= true_mean <= high
    means = rng2.choice(x, size=(2000, 20)).mean(axis=1)
    low, high = np.percentile(means, [2.5, 97.5])
    hits_boot += low <= true_mean <= high
print(hits_t / 400, hits_boot / 400)
```

```text
0.875 0.855
```

"%95" aralıkların ikisi de gerçek değeri yalnızca %87,5 ve
%85,5 oranında yakalıyor. Bootstrap t aralığından iyi değil:
20 gözlemlik bir örneklem, kuyruktaki büyük değerleri çoğu zaman hiç
içermez ve bootstrap ancak örneklemde olanı yeniden örnekleyebilir.
Bootstrap formülün yerine geçer, verinin yerine geçmez.

## Özet

- Bootstrap: örneklemden yerine koyarak yeniden örnekle, istatistiği
  hesapla, ortadaki %95'i al.
- Formülü olmayan istatistikler (medyan, yüzdelik, oranlar) için işe yarar.
- Permütasyon testi: etiketleri karıştır, gerçek farktan uç olanların payı
  p'dir; yalnızca rastgele atamaya dayanır.
- Büyük örneklemde formüllerle aynı sonucu verirler.
- Küçük, çarpık örneklemde bootstrap da güvenilmezdir.
