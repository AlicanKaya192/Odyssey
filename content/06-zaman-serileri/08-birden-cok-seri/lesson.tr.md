# Birden Çok Seri

Şimdiye kadar hep tek bir seriyle çalıştık: bir mağaza, bir sensör, bir hisse.
Gerçek işlerde seri neredeyse hiç tek gelmiyor. Dört mağaza, elli ürün, iki
yüz sensör: aynı ölçüm, farklı birimler için, aynı tabloda.

Bu bölümün sorusu şu: öğrendiğin her şeyi (gecikme, fark, yeniden örnekleme,
pencere) **her seri için ayrı ayrı** nasıl uygularsın, ve serileri birbiriyle
nasıl birleştirirsin?

## İki biçim

Dört mağazanın 2024 satışı (`stores.csv`, 1291 satır):

```text
      date store  sales
2024-01-01     A    291
2024-01-01     B    180
2024-01-01     C    256
2024-01-02     A    288
2024-01-02     B    190
2024-01-02     C    248
```

Bu **uzun** biçim: her satır bir (tarih, mağaza) çifti. Aynı veri **geniş**
biçimde de tutulabiliyor: her mağaza bir sütun, her tarih bir satır.

<figure class="fig">
  <div class="versus">
    <div><h4>Uzun biçim</h4><p>Satır başına bir <b>(tarih, mağaza)</b>.</p><pre><code class="language-text">date        store  sales
2024-05-01      A    269
2024-05-01      B    174
2024-05-01      C    226
2024-05-01      D    106</code></pre></div>
    <div><h4>Geniş biçim</h4><p>Satır başına bir <b>tarih</b>, mağaza başına bir sütun.</p><pre><code class="language-text">date          A    B    C    D
2024-05-01  269  174  226  106
2024-05-02  ...</code></pre></div>
  </div>
  <figcaption>Aynı dört sayı, iki yerleşim. Uzun biçim yeni mağaza gelince satır ekliyor; geniş biçim sütun ekliyor.</figcaption>
</figure>

```python
import pandas as pd

long = pd.read_csv("stores.csv", parse_dates=["date"])
wide = long.pivot(index="date", columns="store", values="sales")

print(wide.shape)               # (366, 4)
print(wide.head(3))
```

```text
store           A      B      C   D
date
2024-01-01  291.0  180.0  256.0 NaN
2024-01-02  288.0  190.0  248.0 NaN
2024-01-03  287.0  191.0  269.0 NaN
```

Geri dönüş `melt`:

```python
back = wide.reset_index().melt(id_vars="date", var_name="store", value_name="sales")
```

İkisi de aynı bilgiyi taşıyor; hangisinin rahat olduğu işe bağlı. Dosyalar ve
veritabanları çoğunlukla uzun biçimde geliyor; karşılaştırma, korelasyon ve
grafik için geniş biçim daha kolay.

## Geniş biçim eksikleri gösteriyor

Uzun tabloda 1291 satır vardı; geniş tabloda 366 × 4 = 1464 hücre var. Aradaki
fark, uzun tabloda **hiç satırı olmayan** (tarih, mağaza) çiftleri:

```python
print(long.groupby("store").size().to_dict())
# {'A': 366, 'B': 366, 'C': 314, 'D': 245}

print(wide.isna().sum().to_dict())
# {'A': 0, 'B': 0, 'C': 52, 'D': 121}

print(wide["D"].first_valid_index().date())     # 2024-05-01
```

Uzun biçimde eksik satır **görünmüyordu**; geniş biçimde `NaN` olarak ortaya
çıktı. Bölüm 03'teki `asfreq` ile aynı etki: tabloyu düzenli bir ızgaraya
oturtmak eksikliği görünür kılıyor.

## Her seri için ayrı: `groupby`

Uzun biçimde en büyük tuzak burada. Dünün satışını getirmek için alışkanlıkla
`shift(1)` yazarsan:

```python
long["lag_wrong"] = long["sales"].shift(1)
print(long.head(5))
```

```text
        date store  sales  lag_wrong
0 2024-01-01     A    291        NaN
1 2024-01-01     B    180      291.0
2 2024-01-01     C    256      180.0
3 2024-01-02     A    288      256.0
4 2024-01-02     B    190      288.0
```

B mağazasının "dünü" olarak A mağazasının **aynı günkü** satışı gelmiş.
`shift` satır kaydırıyor; satırlar mağazalar arasında sırayla dizildiği için
bir önceki satır başka bir mağaza.

Doğrusu, kaydırmayı **her mağazanın kendi içinde** yapmak:

```python
long["lag1"] = long.groupby("store")["sales"].shift(1)
print(long[long["date"] == "2024-01-02"])
```

```text
        date store  sales  lag1
3 2024-01-02     A    288  291.0
4 2024-01-02     B    190  180.0
5 2024-01-02     C    248  256.0
```

Farkı ölçelim:

```python
print(round(long["sales"].corr(long["sales"].shift(1)), 3))   # -0.33
print(round(long["sales"].corr(long["lag1"]), 3))             # 0.866
```

Yanlış gecikmeyle korelasyon **eksi** çıkıyor; doğrusuyla 0.866. **Hata yok**;
yanlış sütun bir modelin içine sessizce girip onu bozuyor.

Kural: **uzun biçimde `shift`, `diff`, `pct_change`, `rolling`, `cumsum` her
zaman `groupby` ile.** Pencere işlemleri için `transform`:

```python
long["ma7"] = long.groupby("store")["sales"].transform(lambda x: x.rolling(7).mean())
```

Geniş biçimde bu tuzak yok: her sütun zaten tek bir seri, işlemler sütun
sütun uygulanıyor (`wide.shift(1)`, `wide.rolling(7).mean()`).

## Her seri için yeniden örnekleme

Uzun biçimde mağaza bazında haftalık toplam için `groupby` ile `Grouper`
birlikte kullanılıyor:

```python
weekly = long.groupby(["store", pd.Grouper(key="date", freq="W")])["sales"].sum()
print(weekly.loc["A"].head(2))
```

```text
date
2024-01-07    2296
2024-01-14    2297
```

`pd.Grouper(key="date", freq="W")` "tarih sütununu haftalık kovalara böl"
demek. Sonuç iki seviyeli bir indeks: mağaza ve hafta. Geniş biçimde aynı iş
tek satır: `wide.resample("W").sum()`.

## Serileri karşılaştırmak

Mağazaların düzeyleri çok farklı:

```python
print(long.groupby("store")["sales"].agg(["sum", "mean", "count"]).round(1))
```

```text
          sum   mean  count
store
A      116462  318.2    366
B       65806  179.8    366
C       78034  248.5    314
D       41877  170.9    245
```

Ham sayılarla "hangisi daha hızlı büyüyor?" sorusu cevaplanamıyor: A her gün
en çok satan mağaza. Hepsini aynı noktadan başlatınca resim değişiyor. Aylık
ortalamaları, dört mağazanın da açık olduğu ilk ay olan Mayıs'ı 100 kabul
ederek endeksle:

```python
monthly = wide.resample("ME").mean()
index = monthly / monthly.loc["2024-05-31"] * 100

print(index.loc["2024-12-31"].round(1).to_dict())
# {'A': 120.3, 'B': 116.8, 'C': 114.1, 'D': 182.2}
```

<figure class="fig">
  <svg viewBox="0 0 680 250" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="195.6" x2="666" y2="195.6"/><text class="dim" x="38" y="199.1" font-size="10.5" text-anchor="end">100</text><line class="grid" x1="44" y1="154.9" x2="666" y2="154.9"/><text class="dim" x="38" y="158.4" font-size="10.5" text-anchor="end">120</text><line class="grid" x1="44" y1="114.2" x2="666" y2="114.2"/><text class="dim" x="38" y="117.7" font-size="10.5" text-anchor="end">140</text><line class="grid" x1="44" y1="73.5" x2="666" y2="73.5"/><text class="dim" x="38" y="77.0" font-size="10.5" text-anchor="end">160</text><line class="grid" x1="44" y1="32.8" x2="666" y2="32.8"/><text class="dim" x="38" y="36.3" font-size="10.5" text-anchor="end">180</text><line class="line" x1="44" y1="220" x2="666" y2="220"/><line class="line" x1="44.0" y1="220" x2="44.0" y2="224"/><text class="dim" x="44.0" y="236" font-size="10.5" text-anchor="middle">May</text><line class="line" x1="132.9" y1="220" x2="132.9" y2="224"/><text class="dim" x="132.9" y="236" font-size="10.5" text-anchor="middle">Haz</text><line class="line" x1="221.7" y1="220" x2="221.7" y2="224"/><text class="dim" x="221.7" y="236" font-size="10.5" text-anchor="middle">Tem</text><line class="line" x1="310.6" y1="220" x2="310.6" y2="224"/><text class="dim" x="310.6" y="236" font-size="10.5" text-anchor="middle">Ağu</text><line class="line" x1="399.4" y1="220" x2="399.4" y2="224"/><text class="dim" x="399.4" y="236" font-size="10.5" text-anchor="middle">Eyl</text><line class="line" x1="488.3" y1="220" x2="488.3" y2="224"/><text class="dim" x="488.3" y="236" font-size="10.5" text-anchor="middle">Eki</text><line class="line" x1="577.1" y1="220" x2="577.1" y2="224"/><text class="dim" x="577.1" y="236" font-size="10.5" text-anchor="middle">Kas</text><line class="line" x1="666.0" y1="220" x2="666.0" y2="224"/><text class="dim" x="666.0" y="236" font-size="10.5" text-anchor="middle">Ara</text><polyline class="curve" style="stroke-width:2.4" points="44.0,195.6 132.9,194.6 221.7,198.7 310.6,186.1 399.4,178.2 488.3,169.5 577.1,159.9 666.0,154.2"/><polyline class="curve2" style="stroke-width:2.4" points="44.0,195.6 132.9,194.0 221.7,191.7 310.6,185.4 399.4,177.3 488.3,168.3 577.1,161.4 666.0,161.3"/><polyline class="curve3" style="stroke-width:2.4" points="44.0,195.6 132.9,195.2 221.7,197.4 310.6,184.7 399.4,185.3 488.3,176.2 577.1,171.0 666.0,167.0"/><polyline class="curve4" style="stroke-width:2.4" points="44.0,195.6 132.9,179.4 221.7,165.9 310.6,131.2 399.4,107.5 488.3,77.2 577.1,50.1 666.0,28.2"/><line class="curve3" stroke-dasharray="4 4" x1="44" y1="195.6" x2="666" y2="195.6"/><line class="curve" x1="54" y1="22" x2="72" y2="22"/><text class="ink" x="78" y="26" font-size="11">A</text><line class="curve2" x1="107" y1="22" x2="125" y2="22"/><text class="ink" x="131" y="26" font-size="11">B</text><line class="curve3" x1="160" y1="22" x2="178" y2="22"/><text class="ink" x="184" y="26" font-size="11">C</text><line class="curve4" x1="213" y1="22" x2="231" y2="22"/><text class="ink" x="237" y="26" font-size="11">D</text></svg>
  <figcaption>Aylık ortalama satış, Mayıs = 100. Ham sayılarda en küçük olan D, endekste en hızlı büyüyen: Aralık'ta 182. Öteki üç mağaza 114–120 arasında; aralarındaki fark yıl sonu mevsimselliğine göre küçük.</figcaption>
</figure>

En küçük mağaza en hızlı büyüyen: D, Mayıs'tan Aralık'a %82 büyümüş. Toplam
içindeki payı da buna göre değişiyor:

```python
quarterly = wide.resample("QE").sum()
share = quarterly.div(quarterly.sum(axis=1), axis=0) * 100
print(share.round(1))
```

```text
store          A     B     C     D
date
2024-03-31  43.8  25.5  30.7   0.0
2024-06-30  39.6  22.3  26.7  11.4
2024-09-30  36.3  20.5  24.2  18.9
2024-12-31  35.7  19.7  22.9  21.7
```

A'nın payı 43.8'den 35.7'ye inmiş. A küçülmedi; pasta büyüdü.

## Birlikte hareket ediyorlar mı?

```python
print(wide.corr().round(2).loc["A"].to_dict())
# {'A': 1.0, 'B': 0.46, 'C': 0.88, 'D': 0.8}

print(wide.resample("W").mean().corr().round(2).loc["A"].to_dict())
# {'A': 1.0, 'B': 0.83, 'C': 0.77, 'D': 0.94}
```

Günlük veride A ile B'nin korelasyonu 0.46; haftalık ortalamada 0.83. Günlük
korelasyon büyük ölçüde **haftalık deseni** ölçüyor: A'nın hafta sonu güçlü,
B'ninki zayıf. Haftalığa inince o desen gidiyor ve geriye ortak trend ile
ortak yıllık desen kalıyor. İki serinin "ilişkili" olması, hangi sıklıkta
baktığına bağlı.

## İki tür eksiklik

Geniş tablodaki `NaN`'lerin hepsi aynı anlama gelmiyor:

<figure class="fig">
  <div class="versus">
    <div><h4>Kapalı: C mağazası, pazarlar</h4><p>Mağaza var, o gün satış <b>yok</b>.<br>Toplamda <b>sıfır</b> saymak doğru.<br>Ortalamada iki seçenek: açık gün başına ya da takvim günü başına.</p></div>
    <div class="no"><h4>Yok: D mağazası, Mayıs öncesi</h4><p>Mağaza henüz <b>açılmamış</b>.<br>Sıfır saymak <b>yanlış</b>: olmayan ayları "kötü ay" yapıyor.<br>Doğrusu o dönemi hesaba katmamak.</p></div>
  </div>
  <figcaption>Tabloda ikisi de <code>NaN</code>. Hangisi olduğunu veri söylemiyor; veriyi tanıyan kişi söylüyor.</figcaption>
</figure>

**C mağazası pazarları kapalı.** O gün kayıt yok, çünkü satış yok. Toplam
alırken sıfır saymak doğru:

```python
print(round(wide["C"].mean(), 1))              # 248.5   acik oldugu gunlerin ortalamasi
print(round(wide["C"].fillna(0).mean(), 1))    # 213.2   takvim gunu basina
```

İki sayı iki farklı soruyu cevaplıyor: "açık olduğu gün ne kadar satıyor?" ve
"günde ortalama ne kadar ciro getiriyor?". İkisi de meşru; hangisini
hesapladığını bilmen gerekiyor.

**D mağazası 1 Mayıs'ta açıldı.** Ondan önceki `NaN` "sıfır satış" değil,
"mağaza yok":

```python
print(round(wide["D"].mean(), 1))              # 170.9
print(round(wide["D"].fillna(0).mean(), 1))    # 114.4   yanlis
```

Sıfırla doldurmak D'nin ortalamasını üçte bir düşürüyor ve olmayan dört ayı
"çok kötü geçen dört ay" gibi gösteriyor.

Toplamda da aynı ayrım:

```python
total = wide.sum(axis=1)
print(total.loc["2024-04-30"], total.loc["2024-05-01"])    # 626.0 775.0
```

`sum` `NaN`'leri atlıyor. Toplam bir gecede 626'dan 775'e sıçradı; satışlar
artmadı, **toplama dördüncü bir mağaza girdi.** Birleşik bir seride böyle bir
sıçrama yapısal kırılmadır; analiz ederken ya aynı mağaza kümesini
karşılaştırırsın (A + B + C) ya da kırılmayı işaretlersin.

## Geçerli olan değeri bulmak: `merge_asof`

A mağazasının birim fiyatı yılda birkaç kez değişiyor. Fiyat listesi yalnızca
**değişiklik günlerini** içeriyor (`prices.csv`):

```text
valid_from  price
2024-01-01   19.9
2024-03-15   21.5
2024-06-01   22.9
2024-09-10   21.9
2024-11-20   24.5
```

Her günün satışını o gün **geçerli olan** fiyatla çarpmak istiyoruz. Sıradan
birleştirme (`merge`) yalnızca tarihi birebir tutan satırları eşliyor:

```python
a = long[long["store"] == "A"][["date", "sales"]]
prices = pd.read_csv("prices.csv", parse_dates=["valid_from"])

exact = a.merge(prices, left_on="date", right_on="valid_from", how="left")
print(exact["price"].notna().sum())        # 5
```

366 günün 5'inde fiyat var. `merge_asof` her satır için **o tarihte ya da
ondan önceki en son** kaydı buluyor:

```python
joined = pd.merge_asof(a, prices, left_on="date", right_on="valid_from")
print(joined[joined["date"].between("2024-03-14", "2024-03-16")])
```

```text
         date  sales valid_from  price
73 2024-03-14    327 2024-01-01   19.9
74 2024-03-15    313 2024-03-15   21.5
75 2024-03-16    426 2024-03-15   21.5
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>13 Mart</span><span>en son fiyat kaydı: <b>1 Ocak</b> → 19.9</span></div>
    <div class="anat-row"><span>14 Mart</span><span>en son fiyat kaydı: <b>1 Ocak</b> → 19.9</span></div>
    <div class="anat-row"><span>15 Mart</span><span>yeni kayıt: <b>15 Mart</b> → 21.5</span></div>
    <div class="anat-row"><span>16 Mart</span><span>en son fiyat kaydı: <b>15 Mart</b> → 21.5</span></div>
  </div>
  <figcaption>Her gün geriye doğru bakıp kendisinden önceki (ya da aynı günkü) en son fiyat değişikliğini buluyor. Beş satırlık fiyat listesi 366 günün hepsine yetiyor.</figcaption>
</figure>

14 Mart hâlâ eski fiyatta, 15 Mart'tan itibaren yeni fiyat geçerli.

```python
joined["revenue"] = joined["sales"] * joined["price"]
print(round(joined["revenue"].sum(), 1))       # 2562737.2
```

`merge_asof` varsayılan olarak **geriye** bakıyor; yani geleceği kullanmıyor.
İki tablonun da tarihe göre sıralı olması gerekiyor. Birden çok seri varsa
`by="store"` eşleştirmeyi mağaza bazında yapıyor.

## Farklı sıklıktaki tabloları birleştirmek

Hedefler aylık verilmiş (`targets.csv`: `month`, `store`, `target`), satış
günlük. Birleştirmenin yolu, sık olanı seyrek olanın sıklığına **indirmek**:

```python
targets = pd.read_csv("targets.csv")

long["month"] = long["date"].dt.to_period("M").astype(str)
actual = long.groupby(["month", "store"])["sales"].sum().reset_index()

report = actual.merge(targets, on=["month", "store"], how="left")
report["pct"] = (report["sales"] / report["target"] * 100).round(1)
print(report[report["month"] == "2024-06"])
```

```text
      month store  sales  target   pct
17  2024-06     A   8926    9580  93.2
18  2024-06     B   4987    5400  92.4
19  2024-06     C   5794    6140  94.4
20  2024-06     D   3994    4450  89.8
```

Anahtar iki sütun: ay ve mağaza. Tersini yapmak (aylık hedefi günlere
kopyalamak) Bölüm 05'teki sıklaştırma tuzağına götürüyor: hedef bir toplam,
günlere kopyalanamaz.

## Sık yapılan hatalar

| Hata | Sonuç | Doğrusu |
|---|---|---|
| Uzun biçimde düz `shift` / `diff` / `rolling` | Başka serinin değeri karışıyor | `groupby("store")` ile |
| Bütün `NaN`'leri sıfırla doldurmak | "Yok" ile "sıfır" karışıyor | Eksikliğin anlamına göre |
| Seri sayısı değişen toplamı analiz etmek | Kırılma büyüme sanılıyor | Aynı kümeyi karşılaştır ya da işaretle |
| Ham düzeylerle büyüme karşılaştırmak | Büyük seri hep "önde" | 100 tabanlı endeks ya da yüzde değişim |
| Günlük korelasyonu ilişki sanmak | Haftalık deseni ölçüyorsun | Deseni çıkar ya da seyrelt |
| Fiyat listesini `merge` ile birleştirmek | Yalnızca değişim günleri eşleşiyor | `merge_asof` |
| Aylık toplamı günlük tabloya kopyalamak | Toplam kat kat sayılıyor | Günlüğü aylığa indir |

## Özet

- **Uzun** biçim: satır başına (tarih, seri). **Geniş** biçim: seri başına
  sütun. `pivot` ve `melt` ikisi arasında geçiyor.
- Geniş biçim, uzun biçimde görünmeyen eksik satırları `NaN` olarak
  gösteriyor.
- Uzun biçimde her zaman serisi işlemi **`groupby` ile**: `shift`, `diff`,
  `rolling`, `resample` (`pd.Grouper`).
- Karşılaştırmak için **endeksle** ya da paya bak; ham düzeyler yanıltıyor.
- `NaN`'in iki anlamı var: **kapalı** (sıfır) ve **yok** (tanımsız). Doldurmadan
  önce hangisi olduğuna karar ver.
- **`merge_asof`** her satıra o tarihte geçerli olan son kaydı getiriyor.
- Farklı sıklıkları birleştirirken sık olanı seyrek olana indir.
