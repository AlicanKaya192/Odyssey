# Rastgele Atama

Bir A/B testinin gücü tek bir fikirden gelir: kimin A'yı, kimin B'yi
göreceğine **şans** karar verir. Böylece iki grup, değişiklik dışında her
bakımdan ortalamada aynı olur ve aradaki fark değişikliğe bağlanabilir.
Bu bölüm, atama rastgele olmayınca ne olduğunu ve gerçek bir sistemde
rastgele atamanın nasıl yapıldığını gösteriyor.

## Kendi seçen gruplar: seçim yanlılığı

Mağaza yeni bir özelliği "isteyen açsın" diye sunmuş olsun. Özellik aslında
**hiçbir şey yapmıyor**. Ama sık gelen kullanıcılar onu daha çok fark edip
açıyor:

```python
import numpy as np
from ab_data import make_user_log

users = make_user_log()
rng = np.random.default_rng(81)
opted = rng.random(len(users)) < np.clip(0.05 * users["sessions"], 0, 0.9)
print(round(opted.mean(), 3))
print(round(users["bought"][opted].mean(), 4),
      round(users["bought"][~opted].mean(), 4))
print(round(users["sessions"][opted].mean(), 2),
      round(users["sessions"][~opted].mean(), 2))
```

```text
0.185
0.163 0.107
6.15 3.21
```

Özelliği açanlar 5,6 puan daha çok satın almış. "Özellik
satışı artırıyor" demek çok kolay, ama yanlış: açanlar zaten daha sık gelen
kullanıcılar (son satır). Fark özellikten değil, **kimin seçtiğinden**
geliyor. Buna **seçim yanlılığı** (selection bias) denir; ziyaret sayısı
burada bir **karıştırıcı değişken** (confounder): hem seçimi hem sonucu
etkiliyor.

## Şans karar verince

Aynı kullanıcıları yazı tura ile bölelim:

```python
in_b = rng.random(len(users)) < 0.5
print(round(in_b.mean(), 3))
print(round(users["bought"][in_b].mean() - users["bought"][~in_b].mean(), 4))
print(round(users["sessions"][in_b].mean(), 2),
      round(users["sessions"][~in_b].mean(), 2))
```

```text
0.5
0.0005
3.75 3.75
```

Ziyaret sayıları neredeyse eşit, satın alma farkı küçük. Tek bir bölmeye
güvenmeyelim; aynı şeyi 500 kez yapalım:

```python
diffs = []
for _ in range(500):
    in_b = rng.random(len(users)) < 0.5
    diffs.append(users["bought"][in_b].mean() - users["bought"][~in_b].mean())
print(round(float(np.mean(diffs)), 4), round(float(np.std(diffs)), 4))
```

```text
0.0002 0.0046
```

Rastgele bölmelerde fark ortalamada sıfır ve tipik olarak yalnızca
0,0046 kadar oynuyor: bu, Tahmin ve Standart Hata bölümündeki
standart hatanın ta kendisi. Kendi seçen gruplardaki fark bunun
12 katı. Rastgele atamada iki grup arasındaki her fark ya
değişiklikten ya da şanstan gelir; şansın ne kadar oynattığını da
hesaplayabiliriz. Hipotez testleri tam olarak buna dayanır.

## Gerçek sistemde atama: özet fonksiyonu

Canlı bir sitede `rng.random()` kullanmak sorun çıkarır: aynı kişi sayfayı
yenileyince başka bir grup görebilir. Bunun yerine kullanıcının kimliğinden
**özet** (hash) hesaplanır ve 0–99 arası bir **kovaya** (bucket) çevrilir:

<figure class="fig">
  <div class="flow">
    <span class="node">Tuz<br><small>checkout-v2</small></span><span class="arrow">→</span>
    <span class="node">Kimlik<br><small>U00001</small></span><span class="arrow">→</span>
    <span class="node">MD5 özeti</span><span class="arrow">→</span>
    <span class="node">Kova<br><small>0–99</small></span><span class="arrow">→</span>
    <span class="node acc">Grup<br><small>&lt;50 ise B</small></span>
  </div>
  <figcaption>Aynı kimlik ve aynı tuz her zaman aynı kovaya düşer; kovalar kimlikten bağımsız ve eşit dağılır.</figcaption>
</figure>

```python
import hashlib


def bucket(user_id, salt):
    digest = hashlib.md5(f"{salt}:{user_id}".encode()).hexdigest()
    return int(digest, 16) % 100


print(bucket("U00001", "checkout-v2"), bucket("U00001", "checkout-v2"))
in_b = np.array([bucket(u, "checkout-v2") < 50 for u in users["user_id"]])
users["group"] = np.where(in_b, "B", "A")
users["mobile"] = (users["platform"] == "mobile").astype(int)
summary = users.groupby("group")[["sessions", "mobile", "bought"]].mean()
print(summary.round(3))
print(users["group"].value_counts().sort_index().to_dict())
```

```text
41 41
       sessions  mobile  bought
group                          
A         3.774   0.605   0.119
B         3.732   0.604   0.116
{'A': 10107, 'B': 9893}
```

- Aynı kişi her seferinde aynı kovaya düşüyor: sayfayı yenilemek grubunu
  değiştirmiyor.
- İki grubun ziyaret sayısı, mobil payı ve satın alma oranı birbirine çok
  yakın: atama kullanıcının özellikleriyle ilişkili değil. Bu tabloya
  **denge tablosu** (balance table) denir; her deneyde ilk bakılan
  şeylerden biri.
- Grup büyüklükleri tam 50/50 değil; o kadar küçük sapma şans. Ne kadar
  sapmanın şans sayılamayacağını A/A Testi ve SRM bölümünde göreceğiz.

`md5` burada güvenlik için değil, kimliği eşit dağılan bir sayıya
çevirmek için kullanılıyor. Python'un yerleşik `hash()` fonksiyonu metinlerde
her çalıştırmada farklı sonuç verir (güvenlik için böyle tasarlanmış); bu
yüzden atamada kullanılmaz.

## Tuz: deneyleri birbirinden ayırmak

**Tuz** (salt) deneyin adıdır. Aynı anda iki deney çalışıyorsa her biri
kendi tuzunu kullanır:

```python
other = np.array([bucket(u, "search-v3") < 50 for u in users["user_id"]])
print(round(float(np.mean(in_b == other)), 3))
```

```text
0.504
```

İki deneyde aynı grubu gören kullanıcıların payı yaklaşık yarı: iki atama
birbirinden bağımsız. İki deney aynı tuzu kullansaydı bu pay 1 olurdu:
birinci deneyin B grubundaki herkes ikincinin de B grubunda olurdu ve iki
değişikliğin etkisi birbirinden ayrılamazdı.

## Atama birimi

Neyin rastgele atanacağı da bir karardır:

- **Kullanıcı:** en yaygını. Kişi her gelişinde aynı sürümü görür.
- **Oturum ya da sayfa gösterimi:** daha çok gözlem verir ama aynı kişi iki
  sürümü de görebilir; kişinin davranışını değiştiren değişikliklerde
  sonuçlar birbirine karışır.
- **Daha büyük birimler** (şehir, mağaza, sınıf): kullanıcılar birbirini
  etkiliyorsa gerekir; Ağ Etkisi ve Karışma bölümünde.

Analiz, atama birimiyle aynı düzeyde yapılır: kullanıcıyla atayıp sayfa
gösterimini tek tek gözlem saymak, gözlemlerin bağımsız olmadığını yok
sayar ve p değerlerini fazla küçük gösterir.

## Özet

- Kendi seçen gruplarda fark, seçimi etkileyen değişkenlerden gelebilir
  (seçim yanlılığı).
- Rastgele atamada fark ya değişiklikten ya da hesaplanabilir şanstan
  gelir.
- Canlıda atama `özet(tuz + kimlik) % 100` ile yapılır: kararlı ve dengeli.
- Her deneyin kendi tuzu olur; denge tablosuna her zaman bakılır.
- Analiz atama birimiyle aynı düzeyde yapılır.
