# Tahmin ve Standart Hata

Gerçek bir işte elinde tek bir örneklem olur ve şu cümleyi kurman gerekir:
"Kullanıcılar ortalama 8,4 dakika kalıyor, **artı eksi şu kadar**." Birinci
kısım tahmin, ikinci kısım tahminin ne kadar güvenilir olduğu. Bu bölümde
ikisini tek örneklemden nasıl hesaplayacağımızı ve "iyi bir tahmin" ne
demek, onu öğreniyoruz.

## Tahminci ve tahmin

- **Tahminci** (estimator): örneklemden bir sayı üreten **kural**. "Örneklem
  ortalamasını al" bir tahmincidir.
- **Tahmin** (estimate): o kuralın elindeki örneklemde verdiği **sayı**.
- **Nokta tahmini** (point estimate): bilinmeyen parametre için tek bir
  sayı. Bir sonraki bölümde onu bir aralığa çevireceğiz.

Bir tahmincinin iyi olup olmadığı tek bir sayıdan anlaşılmaz; kuralın
**binlerce örneklemde** nasıl davrandığına bakılır. Üç özellik aranır:

| Özellik | İngilizcesi | Soru |
|---|---|---|
| Yansızlık | unbiasedness | Ortalamada doğru yere mi düşüyor? |
| Tutarlılık | consistency | Örneklem büyüdükçe gerçeğe yaklaşıyor mu? |
| Etkinlik | efficiency | Aynı veriyle ne kadar az oynuyor? |

## Tek örneklemden standart hata

Merkezi limit teoremi ortalamanın standart hatasını $\sigma / \sqrt{n}$
olarak verdi. Ama $\sigma$'yı (evrenin sapması) bilmiyoruz. Çözüm basit:
onun yerine örneklemin sapması $s$'yi koymak.

$$SE = \dfrac{s}{\sqrt{n}}$$

```python
import numpy as np
from ab_data import make_population

users = make_population()
sample = users.sample(n=100, random_state=21)
x = sample["minutes"]
se = x.std() / np.sqrt(len(x))
print(round(x.mean(), 2), round(x.std(), 2), round(se, 3))
```

```text
8.38 4.86 0.486
```

Bu örneklem "ortalama 8,38 dakika, standart hata 0,486"
diyor. Gerçek ortalama 9,04 ve gerçek standart hata $6{,}13 / \sqrt{100}
\approx 0{,}613$. Tek örneklem hem ortalamayı hem sapmayı biraz küçük
tahmin etmiş. Bu şanssızlık mı, yöntemin kusuru mu? Binlerce örneklemle
bakalım.

## Standart hata tahmini ne kadar güvenilir?

```python
import numpy as np
from ab_data import make_population

users = make_population()
x_all = users["minutes"].to_numpy()
rng = np.random.default_rng(22)
samples = rng.choice(x_all, size=(4000, 100))
means = samples.mean(axis=1)
ses = samples.std(axis=1, ddof=1) / np.sqrt(100)
print(round(x_all.std() / np.sqrt(100), 3), round(means.std(), 3),
      round(ses.mean(), 3))
print(round(np.percentile(ses, 5), 3), round(np.percentile(ses, 95), 3))
```

```text
0.613 0.618 0.606
0.464 0.797
```

- İlk satırda üç sayı: formüldeki gerçek standart hata, 4000 ortalamanın
  gerçekte ne kadar oynadığı ve her örneklemin **kendi** hesapladığı
  standart hataların ortalaması. Üçü de 0,61 civarında: yöntem
  doğru.
- İkinci satır tek tek tahminlerin yayılımı: örneklemlerin %90'ı standart
  hatayı 0,464 ile 0,797 arasında buldu. Bizim tahminimiz
  (0,486) bu aralığın içinde: sıradan bir şanssızlık.
- Çarpık veride az sayıda uzun oturum her örneklemde olmayabilir; o yüzden
  tek tek tahminler gerçeğin altında kalmaya daha yatkın, ortalamada ise
  yakın. Küçük ve çarpık örneklemde standart hata da "tahmin"dir.

## Karekök kuralı: hassasiyetin fiyatı

Standart hata $\sqrt{n}$ ile küçülür. Yani hatayı yarıya indirmek için
**dört kat** veri gerekir. İstenen standart hataya ulaşmak için gereken
örneklem:

$$n = \left(\dfrac{\sigma}{SE_{hedef}}\right)^2$$

```python
import math
from ab_data import make_population

users = make_population()
sigma = users["minutes"].std()
for target in [1.0, 0.5, 0.25]:
    print(target, math.ceil((sigma / target) ** 2))
```

```text
1.0 38
0.5 151
0.25 601
```

- 1 dakikalık hassasiyet için 38 kişi yeter.
- Yarım dakika için 151, çeyrek dakika için 601 kişi:
  her yarılamada dört kat.
- `math.ceil` yukarı yuvarlar: kişi sayısı tam sayı olmalı ve "biraz eksik"
  hedefi tutturmaz.
- Gerçek işte $\sigma$ bilinmez; geçmiş veriden ya da küçük bir ön
  örneklemden tahmin edilir.

## Etkinlik: ortalama mı, medyan mı?

Çan biçimli veride hem ortalama hem medyan merkezi yansız tahmin eder. Hangisi
daha az oynuyor?

```python
import numpy as np
from ab_data import make_population

users = make_population()
y = users["load_ms"].to_numpy()
rng = np.random.default_rng(23)
samples = rng.choice(y, size=(4000, 100))
sd_mean = samples.mean(axis=1).std()
sd_median = np.median(samples, axis=1).std()
ratio = (sd_median / sd_mean) ** 2
print(round(sd_mean, 2), round(sd_median, 2), round(ratio, 2))
```

```text
11.98 14.83 1.53
```

- Aynı 100 kişilik örneklemlerde medyan, ortalamadan daha çok oynadı.
- Son sayı varyansların oranı: medyanın ortalama kadar hassas olması için
  yaklaşık 1,53 kat veri gerekir. Normal dağılımda kuramsal
  değer $\pi / 2 \approx 1{,}57$.
- Çan biçimli veride ortalama daha **etkin** (efficient). Aykırı dolu veride
  tablo tersine dönebilir; o zaman medyanın dayanıklılığı daha değerli.

## Yanlı bir tahminci: örneklemin en büyüğü

En yavaş sayfa açılış süresini 100 kullanıcının en büyüğüyle tahmin edelim:

```python
import numpy as np
from ab_data import make_population

users = make_population()
y = users["load_ms"].to_numpy()
rng = np.random.default_rng(24)
maxes = rng.choice(y, size=(2000, 100)).max(axis=1)
print(y.max(), round(maxes.mean(), 1), (maxes < y.max()).mean())
```

```text
1324 1150.0 0.999
```

Gerçek en yavaş değer 1324 ms; örneklemlerin en büyüğü ortalamada
1150,0 ms ve örneklemlerin %99,9 kadarı gerçeğin
altında kaldı. Örneklem büyüse de bu tahminci gerçeğe **alttan** yaklaşır;
hiç üstüne çıkamaz. Yanlılığın tanımı tam bu: ortalamada aynı yöne sapma.

## Oranlar için aynısı

```python
import numpy as np
from ab_data import make_population

users = make_population()
sample = users["bought"].sample(n=400, random_state=25)
p_hat = sample.mean()
print(round(p_hat, 4), round(np.sqrt(p_hat * (1 - p_hat) / 400), 4))
```

```text
0.1325 0.017
```

400 kişilik bu örneklem "alışveriş yapanların payı 0,1325, standart
hata 0,017" diyor. Gerçek pay 0,114: tahmin ondan yaklaşık
1,1 standart hata uzakta. Bunun olağan mı şaşırtıcı mı olduğunu
bir sonraki bölümde güven aralığıyla, sonra hipotez testiyle soracağız.

## Özet

- Tahminci bir kural, tahmin o kuralın verdiği sayı. İyi tahminci yansız,
  tutarlı ve etkin olur; bunu benzetimle ölçeriz.
- Standart hata tek örneklemden $s / \sqrt{n}$ ile tahmin edilir; küçük ve
  çarpık örneklemde bu tahmin de oynar.
- Hassasiyeti ikiye katlamak dört kat veri ister:
  $n = (\sigma / SE_{hedef})^2$.
- Çan biçimli veride ortalama medyandan etkin; örneklemin en büyüğü ise
  yanlı bir tahmincidir.
