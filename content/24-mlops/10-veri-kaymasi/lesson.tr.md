# Veri Kayması

İzleme bölümünde bir sütunun ortalaması aydan aya kaydı ve tahmin oranı
tırmandı. Ortalama kaba bir ölçü: dağılımın şekli değişirken ortalama
yerinde kalabilir. Bu bölümde bir sütunun dağılımının ne kadar değiştiğini
ölçen iki yaygın yöntemi kendimiz yazıyoruz: **PSI** ve **KS**. Sonra
iki önemli soruya bakıyoruz: büyük veride "anlamlı" fark neden yanıltır,
ve her kayma modele zarar verir mi?

## Veri kayması nedir?

Modelin girdilerinin dağılımı zamanla değişirse buna **veri kayması**
(data drift) denir. Bu modülün verisinde aylar geçtikçe müşteriler
hizmeti daha az kullanıyor ve daha çok ödüyor. Model aynı; gördüğü
müşteriler değişiyor.

Karşılaştırmanın iki tarafı var: **referans** (modelin eğitildiği veri)
ve **güncel** (bu ayın verisi).

```python
from ml_data import make_customers, NUMERIC

reference = make_customers(2000)


def column(rows, name):
    return [r[name] for r in rows]


def month_rows(month):
    return make_customers(1000, seed=99, month=month)


print("reference usage:", round(sum(column(reference, "usage_hours")) / 2000, 1))
print("month 3 usage:", round(sum(column(month_rows(3), "usage_hours")) / 1000, 1))
```

```text
reference usage: 32.2
month 3 usage: 27.5
```

## PSI: kutulara bölüp karşılaştırmak

**PSI** (population stability index, nüfus kararlılık endeksi) şöyle
çalışır:

1. Referans veriyi sıralayıp **eşit kalabalık** on kutuya böl: her kutuda
   referansın yüzde 10'u olsun. Kutu sınırları referansın onda birlik
   dilimleri.
2. Güncel verinin her kutuya düşen payını hesapla.
3. Her kutu için `(güncel - referans) × ln(güncel / referans)` ve topla.

Paylar aynıysa her terim sıfır; ayrıştıkça PSI büyür.

```python
import bisect
import math


def psi(reference, current, bins=10):
    ordered = sorted(reference)
    edges = [ordered[len(ordered) * i // bins] for i in range(1, bins)]

    def shares(values):
        counts = [0] * bins
        for v in values:
            counts[bisect.bisect_left(edges, v)] += 1
        return [max(c / len(values), 0.0001) for c in counts]

    ref, cur = shares(reference), shares(current)
    return sum((c - r) * math.log(c / r) for r, c in zip(ref, cur))


print("month  " + "  ".join(f"{name:>13}" for name in NUMERIC))
for month in [0, 1, 2, 3, 6]:
    current = month_rows(month)
    values = [psi(column(reference, n), column(current, n)) for n in NUMERIC]
    print(f"{month:>5}  " + "  ".join(f"{v:>13.3f}" for v in values))
```

```text
month         tenure    monthly_fee  support_calls    usage_hours
    0          0.012          0.013          0.004          0.016
    1          0.030          0.058          0.026          0.037
    2          0.005          0.229          0.055          0.121
    3          0.012          0.456          0.109          0.284
    6          0.012          1.875          0.280          1.152
```

Kodda üç ayrıntı:

- `edges` dokuz kutu sınırı: sıralı listenin onda biri, onda ikisi...
  noktalarındaki değerler.
- `bisect.bisect_left(edges, v)` bir değerin kaçıncı kutuya düştüğünü
  buluyor: `v`'den küçük kaç sınır varsa o numaralı kutu. Sıralı listede
  yer arayan hızlı bir fonksiyon.
- Boş bir kutuda pay sıfır olur ve `log(0)` tanımsızdır; bu yüzden payı
  en az `0.0001` yapıyoruz.

Tabloyu okurken yaygın bir başparmak kuralı (kanun değil):

| PSI | Yorum |
|---|---|
| 0,1'in altı | Kararlı |
| 0,1 – 0,25 | Orta kayma, bak |
| 0,25'in üstü | Büyük kayma |

0. ay satırı önemli: aynı aydan **başka bir örneklem**. Hiçbir şey
değişmediği hâlde PSI sıfır değil (0,01 civarı): örneklemin
şansı. Kayma bu gürültü düzeyinin belirgin üstünde olunca anlamlı. Ücret
2. aydan itibaren, kullanım 3. aydan itibaren büyük kayma gösteriyor;
abonelik süresi hiç kaymıyor.

## KS: en büyük aralık

İkinci yöntem **Kolmogorov-Smirnov** (KS) testi. Her iki veri için
"değerlerin kaçta kaçı `x`'ten küçük ya da eşit?" eğrisini (birikimli
dağılım) çizip iki eğri arasındaki **en büyük dikey uzaklığa** bakar.
Bu uzaklık KS **istatistiği**: 0 ile 1 arasında, aynı dağılımlarda sıfıra
yakın. Kendimiz yazıp SciPy'ninkiyle karşılaştıralım:

```python
from scipy.stats import ks_2samp


def ks_statistic(a, b):
    a, b = sorted(a), sorted(b)
    gaps = []
    for x in sorted(set(a) | set(b)):
        share_a = bisect.bisect_right(a, x) / len(a)
        share_b = bisect.bisect_right(b, x) / len(b)
        gaps.append(abs(share_a - share_b))
    return max(gaps)


ref_usage = column(reference, "usage_hours")
month1_usage = column(month_rows(1), "usage_hours")
print("ours:", round(ks_statistic(ref_usage, month1_usage), 4))
print("scipy:", round(float(ks_2samp(ref_usage, month1_usage).statistic), 4))
```

```text
ours: 0.0805
scipy: 0.0805
```

İkisi aynı. `bisect_right(a, x)` sıralı listede `x`'ten küçük ya da eşit
kaç değer olduğunu veriyor; listenin boyuna bölünce pay. Kümelerin
birleşimi (`|`) iki verideki bütün değerleri bir kez geziyor.

## p-değeri tuzağı

`ks_2samp` bir de **p-değeri** veriyor: "iki örneklem aynı dağılımdan
gelseydi bu kadar büyük bir fark ne sıklıkla çıkardı?" Küçükse fark
"istatistiksel olarak anlamlı" denir. Ama p-değeri örneklem büyüdükçe
küçülür. Aynı küçük kaymayı (0. aydan 1. aya kullanım) üç farklı
büyüklükte ölçelim:

```python
for n in [200, 2000, 50000]:
    a = column(make_customers(n, seed=1), "usage_hours")
    b = column(make_customers(n, seed=2, month=1), "usage_hours")
    result = ks_2samp(a, b)
    statistic, p_value = result.statistic, result.pvalue
    print(f"n={n:>6}  statistic {statistic:.3f}  p-value {p_value:.2g}")
```

```text
n=   200  statistic 0.095  p-value 0.33
n=  2000  statistic 0.083  p-value 2.1e-06
n= 50000  statistic 0.076  p-value 1.2e-124
```

Kaymanın büyüklüğü (istatistik) üç satırda da hemen hemen aynı. p-değeri
ise 200 müşteride "anlamsız", 50 000 müşteride akıl almaz derecede
"anlamlı". Canlı sistemlerde veri çoktur; p-değerine bakan bir uyarı en
küçük, önemsiz kaymada bile çalar. Bu yüzden izlemede **büyüklük
ölçüleri** (PSI, KS istatistiği) kullanılır ve eşik ona konur.

`:.2g` sayıyı iki anlamlı basamakla yazıyor; çok küçük sayıları üslü
biçimde (`1.2e-124`).

## Her kayma zarar verir mi?

İzleme bölümündeki doğruluk tablosunu hatırla. Ücretin PSI'si 3. ayda
0,456: tabloya göre "büyük kayma". O ay modelin doğruluğu ise
hâlâ 0,784, eğitimdekine yakın. Doğruluk asıl 4. ayda düştü.

Neden? Çünkü bu modülün verisinde ücret ve kullanım değişse de müşterinin
**nasıl** karar verdiği 4. aya kadar aynı: yüksek ücret ve az kullanım
hâlâ aynı oranda iptale götürüyor. Model bu ilişkiyi öğrenmiş; girdiler
kaysa bile ilişki geçerli olduğu sürece doğru tahmin ediyor. 4. ayda
değişen ilişkinin kendisi; bu da bir sonraki bölümün konusu: **kavram
kayması**.

Bu yüzden:

- Veri kayması bir **uyarıdır**, kendi başına yeniden eğitme nedeni
  değildir.
- Önce modelin çok güvendiği sütunlardaki kaymaya bakılır; önemsiz bir
  sütundaki büyük kayma çoğu zaman zararsızdır.
- Asıl karar, etiketler gelince ölçülen **kaliteye** göre verilir.

## Kategorik sütunlar

PSI'nin kutuları sayısal sütunlar için. Paket gibi kategorik bir sütunda
kutular zaten hazır: her kategori bir kutu. Aynı formül kategorilerin
paylarıyla uygulanır. Bu modülün verisinde `pro` payı aylar boyunca
yaklaşık yüzde 40'ta kalıyor; paket kaymıyor.

## Özet

- **Veri kayması**: modelin girdilerinin dağılımının zamanla değişmesi.
- **PSI**: referansı eşit kalabalık kutulara böl, güncel payları
  karşılaştır. 0,1'in altı kararlı, 0,25'in üstü büyük kayma (başparmak
  kuralı).
- Aynı aydan başka bir örneklemin PSI'si sıfır değildir: önce gürültü
  düzeyini bil.
- **KS istatistiği**: iki birikimli dağılım arasındaki en büyük uzaklık.
- **p-değeri** büyük örneklemde her küçük farkı "anlamlı" gösterir;
  izlemede büyüklük ölçüsü kullanılır.
- Her kayma zarar vermez: girdiler kaysa da ilişki aynıysa model iyi
  kalır. Karar kaliteye göre verilir.
