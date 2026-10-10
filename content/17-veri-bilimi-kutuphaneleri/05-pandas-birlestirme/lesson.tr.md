# pandas ile Birleştirme

Gerçek veri tek tabloda gelmez: siparişler bir dosyada, müşteriler başka bir
dosyada, her ayın satışı ayrı bir tabloda. Bunları birleştirmenin üç yolu
var: anahtar sütunla eşleştirmek (`merge`), alt alta ya da yan yana eklemek
(`concat`) ve indeks üzerinden eşleştirmek (`join`). Birleştirme pandas'ta
en çok sessiz hatanın çıktığı yer: satırlar kaybolur ya da çoğalır, toplamlar
kayar ve hiçbir hata mesajı gelmez. Bu bölüm hem yolları hem de bu
hataları yakalamanın yollarını anlatıyor.

## merge ve dört birleştirme türü

```python
import pandas as pd

orders = pd.DataFrame({"order": [1, 2, 3, 4], "customer": [10, 20, 10, 40],
                       "amount": [250, 90, 40, 70]})
customers = pd.DataFrame({"customer": [10, 20, 30], "name": ["Ada", "Can", "Eda"]})
for how in ["inner", "left", "right", "outer"]:
    joined = orders.merge(customers, on="customer", how=how)
    print(how, len(joined), joined["order"].tolist())
print(orders.merge(customers, on="customer", how="left"))
```

```text
inner 3 [1, 2, 3]
left 4 [1, 2, 3, 4]
right 4 [1.0, 3.0, 2.0, nan]
outer 5 [1.0, 3.0, 2.0, nan, 4.0]
   order  customer  amount name
0      1        10     250  Ada
1      2        20      90  Can
2      3        10      40  Ada
3      4        40      70  NaN
```

`on="customer"` iki tabloda da aynı adla duran **anahtar** sütun. Müşteri
40'ın kaydı yok, müşteri 30'un siparişi yok; `how` bu eşleşmeyenlere ne
olacağını seçer:

| `how` | Kalan satırlar | Burada |
|---|---|---|
| `inner` (varsayılan) | yalnızca iki tarafta da olan anahtarlar | sipariş 4 **kayboldu** |
| `left` | soldakilerin hepsi | sipariş 4 var, adı `NaN` |
| `right` | sağdakilerin hepsi | Eda var, siparişi `NaN` |
| `outer` | ikisinin hepsi | 5 satır |

- Varsayılan `inner`: eşleşmeyen sipariş **sessizce** düşer. Siparişlere bilgi
  eklerken neredeyse her zaman istenen `how="left"`'tir; satır sayısı
  değişmemeli.
- Bir tarafta olmayan değer `NaN` olur; `right` ve `outer`'da `order`
  sütunu bu yüzden ondalığa döndü.

## indicator: kaybolanı bul

```python
import pandas as pd

orders = pd.DataFrame({"order": [1, 2, 3, 4], "customer": [10, 20, 10, 40],
                       "amount": [250, 90, 40, 70]})
customers = pd.DataFrame({"customer": [10, 20, 30], "name": ["Ada", "Can", "Eda"]})
check = orders.merge(customers, on="customer", how="outer", indicator=True)
print(check["_merge"].value_counts().to_dict())
lost = check.loc[check["_merge"] == "left_only", "order"].astype(int).tolist()
print(lost)
```

```text
{'both': 3, 'left_only': 1, 'right_only': 1}
[4]
```

- `indicator=True` her satıra `_merge` sütunu ekler: `both`, `left_only`
  (yalnızca solda), `right_only` (yalnızca sağda).
- Bir birleştirmeden önce `outer` + `indicator` ile bakmak, hangi
  kayıtların eşleşmediğini **adıyla** gösterir: burada sipariş 4'ün müşterisi
  müşteri tablosunda yok. Veri temizliğinde ilk sorulacak soru budur.

## Satır patlaması ve validate

```python
import pandas as pd

orders = pd.DataFrame({"customer": [10, 10, 20], "amount": [250, 40, 90]})
cities = pd.DataFrame({"customer": [10, 10, 20],
                       "city": ["Izmir", "Ankara", "Bursa"]})
joined = orders.merge(cities, on="customer")
print(len(orders), len(joined))
print(int(joined["amount"].sum()), int(orders["amount"].sum()))
try:
    orders.merge(cities, on="customer", validate="many_to_one")
except pd.errors.MergeError as error:
    print("MergeError:", str(error).splitlines()[0])
```

```text
3 5
670 380
MergeError: Merge keys are not unique in right dataset; not a many-to-one merge
```

- Müşteri 10 sağ tabloda **iki kez** geçiyor (iki şehir). merge her eşleşen
  çifti bir satır yapar: müşteri 10'un 2 siparişi × 2 şehri = 4 satır.
  3 satırlık tablo 5 oldu.
- Sonuç: ciro toplamı 380 yerine **670**. Hata yok, rapor yanlış.
- `validate` birleştirmenin türünü önceden söyler ve tutmazsa durdurur:
  `"one_to_one"`, `"one_to_many"`, `"many_to_one"`, `"many_to_many"`.
  Siparişlere müşteri bilgisi eklerken doğru tür `many_to_one`: çok sipariş,
  her siparişe **bir** müşteri.
- Kısa denetim: `len(joined) == len(orders)` olmalı.

## Anahtarın türü ve farklı adlar

```python
import pandas as pd

sales = pd.DataFrame({"product_id": [1, 2], "qty": [3, 5]})
products = pd.DataFrame({"id": ["1", "2"], "title": ["pen", "cup"]})
try:
    sales.merge(products, left_on="product_id", right_on="id")
except ValueError as error:
    print("ValueError:", str(error).split(".")[0])
products["id"] = products["id"].astype(int)
joined = sales.merge(products, left_on="product_id", right_on="id")
print(joined.columns.tolist())
```

```text
ValueError: You are trying to merge on int64 and str columns for key 'product_id'
['product_id', 'qty', 'id', 'title']
```

- Anahtarın adı iki tabloda farklıysa `left_on` / `right_on`. Sonuçta iki
  sütun da kalır; gerekmeyeni `drop(columns="id")` ile atılır.
- Bir tabloda `1` sayı, ötekinde `"1"` metin: pandas bunları eşleştirmez ve
  hata verir. CSV'den okunan kodlarda çok sık olur (öndeki sıfırlar yüzünden
  biri metin okunmuştur). Önce türleri eşitle: `astype(int)` ya da
  `astype(str)`.

## Aynı adlı sütunlar: suffixes

```python
import pandas as pd

jan = pd.DataFrame({"city": ["Izmir", "Ankara"], "sales": [80, 120]})
feb = pd.DataFrame({"city": ["Ankara", "Izmir"], "sales": [110, 95]})
both = jan.merge(feb, on="city")
print(both.columns.tolist())
both = jan.merge(feb, on="city", suffixes=("_jan", "_feb"))
print(both)
```

```text
['city', 'sales_x', 'sales_y']
     city  sales_jan  sales_feb
0   Izmir         80         95
1  Ankara        120        110
```

- Anahtar dışında aynı adla duran sütunlar `_x` ve `_y` ekiyle ayrılır.
  Hangisinin hangisi olduğu iki satır sonra unutulur.
- `suffixes=("_jan", "_feb")` anlamlı ad verir. Sıralar farklı olsa da şehir
  şehirle eşleşti; merge sıraya değil anahtara bakar.

## concat: alt alta eklemek

```python
import pandas as pd

jan = pd.DataFrame({"city": ["Izmir", "Ankara"], "sales": [80, 120]})
feb = pd.DataFrame({"city": ["Bursa"], "sales": [50], "returns": [2]})
stacked = pd.concat([jan, feb])
print(stacked.index.tolist(), stacked.columns.tolist())
print(pd.concat([jan, feb], ignore_index=True).index.tolist())
months = pd.concat([jan, feb], keys=["jan", "feb"])
print(months.loc["feb", "city"].tolist(), months["returns"].isna().sum())
```

```text
[0, 1, 0] ['city', 'sales', 'returns']
[0, 1, 2]
['Bursa'] 2
```

- `concat` eşleştirme yapmaz, **ekler**. Aynı yapıdaki parçaları (her ayın
  dosyası) tek tabloya toplamanın yolu.
- İndeksler olduğu gibi kalır: `[0, 1, 0]`, yani **tekrarlı** etiket (önceki
  bölümün tuzağı). `ignore_index=True` yeniden 0'dan numaralar.
- `keys=` her parçaya bir dış düzey ekler: sonuç MultiIndex'li, hangi satırın
  hangi aydan geldiği belli.
- Sütunlar birleşir; bir parçada olmayan sütun (`returns`) ötekinin
  satırlarında `NaN` olur: 2 eksik.
- Döngüde tek tek eklemek yerine parçaları bir listeye toplayıp **bir kez**
  `concat` çağırmak gerekir; her eklemede bütün tablo yeniden kopyalanır.

## join: indeks üzerinden

```python
import pandas as pd

price = pd.DataFrame({"price": [10.0, 4.5]}, index=["pen", "cup"])
stock = pd.DataFrame({"stock": [3, 8, 1]}, index=["cup", "pen", "box"])
print(price.join(stock))
print(stock.join(price, how="inner").index.tolist())
```

```text
     price  stock
pen   10.0      8
cup    4.5      3
['cup', 'pen']
```

- `join` iki tabloyu **indeksleriyle** eşleştirir; anahtar zaten indeksteyse
  merge'ün kısa yolu. Varsayılanı `how="left"`.
- `price.join(stock)`: kalem 8, fincan 3 stokla eşleşti; kutunun fiyatı
  olmadığı için soldaki tabloda yer almadı.

## Özet

- `merge` anahtar sütunla eşleştirir. Varsayılan `inner` eşleşmeyeni atar;
  bilgi eklerken `how="left"`.
- `indicator=True` eşleşmeyenleri gösterir; `validate=` satır patlamasını
  önceden durdurur. Birleştirmeden sonra satır sayısını kontrol et.
- Anahtar türleri eşit olmalı; farklı adlar `left_on` / `right_on`, aynı adlı
  sütunlar `suffixes`.
- `concat` alt alta ekler (`ignore_index`, `keys`), `join` indeksle eşleştirir.
