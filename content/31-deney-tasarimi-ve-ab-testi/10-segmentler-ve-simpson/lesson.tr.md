# Segmentler ve Simpson Paradoksu

Test bitince ilk merak edilen şey genellikle "kimde işe yaradı?" olur:
mobilde mi, masaüstünde mi, hangi ülkede? Segmentlere bakmak değerlidir
ama iki tuzağı var. Birincisi, grupların bileşimi segmentten segmente
değişirse toplam sonuç segmentlerin söylediğinin **tersini** söyleyebilir:
**Simpson paradoksu**. İkincisi, yeterince segmente bakan biri şans eseri
çarpıcı bir segment bulur.

## Toplamda kaybeden, her haftada kazanan

İki hafta süren bir testte B'nin trafik payı ilk hafta %10, ikinci hafta
%50 yapılmış (yavaş açılış, ramp-up). İlk haftada bir indirim kampanyası
vardı ve herkes daha çok satın aldı. Veriyi biz ürettik: B iki haftada da
satın almayı gerçekten %5 artırıyor.

```python
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
from ab_data import make_ramp_test, make_segment_test

ramp = make_ramp_test()
print(ramp.groupby("group")["bought"].agg(["mean", "size"]).round(4))
k = ramp.groupby("group")["bought"].sum()
n = ramp.groupby("group").size()
p = proportions_ztest([k["B"], k["A"]], [n["B"], n["A"]])[1]
print(f"{p:.1e}")
```

```text
         mean   size
group               
A      0.0952  28059
B      0.0642  11941
5.0e-24
```

Toplamda B'nin satın alma oranı %6,4, A'nınki %9,5; p
değeri çok küçük. Rapor "B satın almayı belirgin biçimde düşürüyor" diye
yazılacak gibi duruyor. Haftalara ayıralım:

```python
by_week = ramp.groupby(["week", "group"])["bought"].mean().unstack()
print(by_week.round(4))
print(ramp.groupby(["week", "group"]).size().unstack())
```

```text
group       A       B
week                 
1      0.1198  0.1215
2      0.0514  0.0525
group      A     B
week              
1      17976  2024
2      10083  9917
```

Her iki haftada da B, A'dan biraz **önde**. Toplamdaki ters sonuç
ağırlıklardan geliyor: B kullanıcılarının çoğu satın almanın düşük olduğu
ikinci haftadan, A kullanıcılarının çoğu ise kampanyalı ilk haftadan.
Toplam oran B için "çoğu ikinci haftadan", A için "çoğu ilk haftadan" bir
ortalama; iki grup aynı karışımla karşılaştırılmıyor.

Bu yüzden atama oranı test ortasında değiştirilen bir deneyde toplamlar
karşılaştırılmaz. A/A Testi ve Örneklem Oranı Uyumsuzluğu bölümündeki SRM
denetimi her hafta ayrı yapılsaydı bu fark hemen görünürdü.

## Doğru karşılaştırma: tabaka içinde

Çözüm, her haftayı kendi içinde karşılaştırıp farkları **aynı
ağırlıklarla** birleştirmektir (tabakalı tahmin). Ağırlık, her haftanın
toplam kullanıcı payıdır; iki grup için aynıdır:

```python
weights = ramp.groupby("week").size() / len(ramp)
print(round(((by_week["B"] - by_week["A"]) * weights).sum(), 4))
```

```text
0.0015
```

Tabakalı fark pozitif: işaret döndü. Bunu tek bir veriye bağlamayalım;
aynı tasarımı 100 farklı tohumla kuralım:

```python
pooled_worse, strat = 0, []
for s in range(100):
    t = make_ramp_test(seed=1000 + s)
    w = t.groupby(["week", "group"])["bought"].mean().unstack()
    m = t.groupby("group")["bought"].mean()
    pooled_worse += m["B"] < m["A"]
    share = t.groupby("week").size() / len(t)
    strat.append(((w["B"] - w["A"]) * share).sum())
print(pooled_worse, round(float(np.mean(strat)), 4))
```

```text
100 0.0043
```

Toplam oran B'yi 100 testin 100 tanesinde geride gösteriyor.
Tabakalı tahminin ortalaması (0,0043) ise gerçek farka
(0,0042) yakın. Daha basit bir yol da var: yalnızca atama oranının
sabit olduğu dönemi (ikinci hafta) çözümlemek.

## Segment avı

İkinci tuzak, ayrıntıya inmek. 40 000 kişilik bir testi 8 ülke × 2 platform
= 16 segmente bölelim. Bu veride B **her segmentte** satın almayı aynı
oranda, %8 artırıyor:

```python
seg = make_segment_test()
cells = seg.groupby(["country", "platform", "group"])["bought"].mean().unstack()
lift = (cells["B"] / cells["A"] - 1).sort_values()
print(lift.round(3).iloc[[0, 1, -2, -1]].to_string())
overall = seg.groupby("group")["bought"].mean()
print(round(overall["B"] / overall["A"] - 1, 3))
```

```text
country  platform
TR       desktop    -0.179
BR       desktop    -0.163
TR       mobile      0.415
US       mobile      0.535
0.115
```

Etki her yerde aynı olduğu hâlde segment tahminleri %-17,9 ile
%53,5 arasında dağılıyor. Bir segment yaklaşık 2500 kişi; bu
kadar küçük gruplarda oran farkı çok gürültülüdür. Raporda "B bu ülkenin
masaüstünde satışı düşürüyor, şu ülkenin mobilinde iki katına
çıkarıyor" yazmak, gürültüyü hikâyeye çevirmektir.

En çarpıcı segment ne kadar yanıltır? Aynı testi 100 kez kurup her
seferinde **en büyük** segment artışını alalım:

```python
best = []
for s in range(100):
    t = make_segment_test(seed=2000 + s)
    c = t.groupby(["country", "platform", "group"])["bought"].mean().unstack()
    best.append((c["B"] / c["A"] - 1).max())
print(round(float(np.mean(best)), 3))
```

```text
0.515
```

Gerçek etki %8 iken "en iyi segment" ortalamada %51,5
görünüyor. Güç Analizi bölümündeki kazananın laneti burada da çalışıyor:
16 tahminin en büyüğünü seçmek, şansın en çok yardım ettiğini seçmektir.

## Segmentler nasıl okunur?

- Karar **toplam** sonuca göre verilir (bileşim aynıysa); segmentler
  açıklamak içindir.
- Segment analizi önceden yazılır ve sayısı az tutulur; Çoklu
  Karşılaştırma bölümündeki düzeltmeler uygulanır.
- Bir segment gerçekten farklı görünüyorsa bu, yeni bir testin
  **sorusudur**.
- Atama oranı segmentten segmente ya da zamanla değiştiyse toplamlar değil
  tabaka içi farklar karşılaştırılır.

## Özet

- Simpson paradoksu: grupların bileşimi farklıysa toplam sonuç her
  tabakadakinin tersi olabilir.
- Atama oranı test ortasında değişirse tabakalı tahmin ya da yalnızca sabit
  oranlı dönem kullanılır.
- Küçük segmentlerin tahminleri çok gürültülüdür; en çarpıcı segment etkiyi
  büyük ölçüde abartır.
- Segmentler açıklar, karar vermez.
