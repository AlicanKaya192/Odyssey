# Ağ Etkisi ve Karışma

Şimdiye kadarki her çözümleme sessiz bir varsayıma dayanıyordu: bir
kullanıcının sonucu yalnızca **kendi** grubuna bağlıdır, başkasının hangi
grupta olduğuna değil. Bu varsayımın adı **SUTVA**'dır (stable unit
treatment value assumption). Kullanıcılar aynı kaynağı paylaştığında
(sürücüler, stok, reklam bütçesi) ya da birbirini etkilediğinde (mesaj,
paylaşım, arkadaş ağı) varsayım bozulur: B'deki biri A'daki birinin
sonucunu değiştirir. Buna **karışma** (interference) denir. Bu bölüm,
karışma olan bir pazarda sıradan A/B testinin ne kadar yanıldığını ölçüyor.

## Paylaşılan sürücüler

Bir araç paylaşım uygulamasında B, yolcuların daha çok yolculuk istemesini
sağlayan bir indirim. Her şehirde sürücü sayısı sabit; istekler sürücüleri
aşınca şehirdeki **herkesin** isteği daha az karşılanır. Veriyi biz
ürettik: 100 şehir, şehir başına 300 yolcu.

```python
import numpy as np
from scipy import stats
from ab_data import make_market


def lift(table, column="completed"):
    m = table.groupby("group")[column].mean()
    return round(float(m["B"] / m["A"] - 1), 3)


market = make_market()
print(lift(market, "requested"), lift(market))
```

```text
0.177 0.181
```

Yolcuları tek tek atayan test, B'nin istekleri %17,7,
tamamlanan yolculukları %18,1 artırdığını söylüyor. Ürün ekibi
"indirim yolculukları beşte bir artırıyor" diye okur.

## Gerçek etki: herkes A ya da herkes B

Aynı pazarı iki dünyada kuralım: herkesin A olduğu ve herkesin B olduğu.
Gerçek etki, bu iki dünyanın tamamlanan yolculuk farkıdır:

```python
all_a = make_market(share_b=0.0)
all_b = make_market(share_b=1.0)
print(round(all_b["completed"].sum() / all_a["completed"].sum() - 1, 3))
a_riders = market.loc[market["group"] == "A", "completed"].mean()
print(round(a_riders / all_a["completed"].mean() - 1, 3))
```

```text
0.012
-0.071
```

İndirim herkese verilseydi yolculuklar yalnızca %1,2 artardı:
sürücü sayısı değişmediği için fazladan istekler büyük ölçüde
karşılanamazdı. Testteki %18,1 nereden geldi? İkinci satır
cevabı veriyor: testteki A yolcuları, herkesin A olduğu dünyaya göre
%7,1 daha az yolculuk yaptı. B yolcuları sürücüleri A
yolcularından **aldı**. Test, B'nin kazancını ve A'nın kaybını birlikte
ölçtü; ikisinin farkı gerçek etkinin çok üstünde.

## Küme halinde atama: şehir şehir

Karışma şehrin içinde kalıyorsa çözüm, atamayı karışmanın sınırında
yapmaktır: her şehrin **bütün** yolcuları ya A ya B olur. Analiz de şehir
düzeyinde yapılır, çünkü atanan birim artık şehirdir:

```python
cities = make_market(design="city")
per_city = cities.groupby(["city", "group"])["completed"].mean().reset_index()
b = per_city.loc[per_city["group"] == "B", "completed"]
a = per_city.loc[per_city["group"] == "A", "completed"]
print(len(a), len(b), round(float(b.mean() / a.mean() - 1), 3))
print(round(float(stats.ttest_ind(b, a, equal_var=False).pvalue), 3))
```

```text
50 50 -0.021
0.709
```

Şehir tasarımı %-2,1 buldu ve anlamlı değil. Tek bir sonuca
bakmak yine yanıltabilir; üç yöntemi 100 farklı pazarda karşılaştıralım:

```python
user_l, city_l, true_l = [], [], []
for s in range(3000, 3100):
    user_l.append(lift(make_market(seed=s)))
    city_l.append(lift(make_market(seed=s, design="city")))
    a0 = make_market(seed=s, share_b=0.0)["completed"].sum()
    b1 = make_market(seed=s, share_b=1.0)["completed"].sum()
    true_l.append(b1 / a0 - 1)
for name, v in [("user", user_l), ("city", city_l), ("true", true_l)]:
    print(name, round(float(np.mean(v)), 3), round(float(np.std(v)), 3))
```

```text
user 0.197 0.015
city 0.016 0.069
true 0.011 0.003
```

Sütunlar: ortalama tahmin ve tahminin pazardan pazara oynaması.

- Kullanıcı tasarımı **her pazarda** yaklaşık %19,7 diyor;
  gerçek ortalamada %1,1. Yanlılık çok büyük ama gürültü
  küçük: yanlış cevabı büyük bir güvenle veriyor.
- Şehir tasarımı ortalamada %1,6 ile gerçeğe yakın, ama
  tahmini pazardan pazara %6,9 oynuyor: 100 şehir, 30 000
  kullanıcıdan çok daha az bilgi taşır.

Bu, karışmanın temel ödünleşimidir: **yansız ama gürültülü** küme tasarımı
ile **gürültüsüz ama yanlı** kullanıcı tasarımı. Yanlılık örneklem
büyütülerek düzelmez; gürültü düzelir.

## Karışmayı nerede beklemeli?

- **Paylaşılan kaynak:** sürücü, kurye, stok, otel odası, reklam bütçesi.
  B'nin fazladan aldığı A'dan eksilir.
- **Sosyal ağ:** B'deki biri bir şey paylaşınca A'daki arkadaşı da
  etkilenir; bu kez etki A'ya **taşar** ve test etkiyi küçük gösterir.
- **İki taraflı pazar:** alıcıya yapılan değişiklik satıcıların
  davranışını değiştirir.

Önlemler: küme halinde atama (şehir, bölge, arkadaş kümesi), zaman
dilimleriyle sırayla açıp kapatma (switchback) ve test öncesinde "bu
değişiklik başkasının sonucunu değiştirebilir mi?" sorusunu plana yazmak.

## Özet

- SUTVA: bir kullanıcının sonucu yalnızca kendi grubuna bağlıdır;
  paylaşılan kaynak ve ağlar bunu bozar.
- Paylaşılan kaynakta kullanıcı düzeyindeki test etkiyi büyütür: B, A'dan
  alır.
- Küme halinde atama yanlılığı giderir; analiz küme düzeyinde yapılır ve
  gürültü büyür.
- Yanlılık daha çok kullanıcıyla düzelmez.
