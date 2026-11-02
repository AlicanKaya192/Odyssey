Merkezi limit teoremi güçlüdür ama koşulsuz değildir. Üç durumda bozulur.

## 1. Değerler bağımsız değilse

Aynı kullanıcının on oturumunu on ayrı kişi gibi saymak örneklemi
olduğundan büyük gösterir. Bu on oturum birbirine benzer: aynı kişinin
alışkanlığını taşır. Gerçek bilgi on kişi kadar değil, bir kişiden biraz
fazlasıdır. Standart hata formülü $n = 10$ alır ve oynamayı küçük tahmin
eder.

**Kontrol:** Bir satır neyi temsil ediyor? Kişiyi mi, olayı mı? Rastgele
seçilen birim (kullanıcı) ile ölçülen birim (oturum) aynı mı?

## 2. Varyans sonlu değilse

Bazı dağılımların kuyruğu o kadar kalındır ki varyansları sonsuzdur. En
bilineni **Cauchy dağılımı**. Örneklem büyüse de ortalamaları
toplanmaz:

```python
import numpy as np

rng = np.random.default_rng(8)
for n in [10, 1000]:
    means = rng.standard_cauchy(size=(2000, n)).mean(axis=1)
    q1, q3 = np.percentile(means, [25, 75])
    print(n, round(q3 - q1, 2))
```

```text
10 2.12
1000 2.04
```

Ortalamaların ortadaki yarısının genişliği (IQR) 10 kişide de 1000 kişide
de yaklaşık 2. Normal veride aynı deney 100 kat büyük örneklemde 10 kat
daralırdı. Gerçek veride bu kadar uç bir durum seyrektir, ama çok kalın
kuyruklu metriklerde (birkaç kullanıcının dev harcama yaptığı gelir verisi)
benzer bir yavaşlık görülür.

## 3. Örneklem küçük ve veri çarpıksa

Teorem "$n$ büyüdükçe" der. Küçük $n$'de çarpık verinin ortalamaları da
çarpıktır; bu bölümde 30 kişilik harcama ortalamalarının hiç aşağı
kaçmadığını gördük.

**Kontrol:** Benzetimle ortalamaları çiz. Yapamıyorsan bootstrap (ikinci
modül) ya da dağılıma dayanmayan yöntemler (parametrik olmayan testler)
kullan.
