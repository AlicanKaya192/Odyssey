# dask

Bölüm 3'te bir dosyayı elle parçalara bölüp her parçada özet çıkardık,
özetleri de kendimiz birleştirdik. Bölüm 10'da işi süreçlere ve iş
parçacıklarına elle dağıttık. **dask** bu iki işi birden, pandas'a çok
benzeyen bir yazımla kendisi yapıyor:

- Tabloyu **bölümlere** (*partition*) ayırıyor; her bölüm sıradan bir pandas
  tablosu.
- Yazdığın işlemleri hemen yapmıyor, bir **görev grafiği** olarak
  kaydediyor.
- `compute()` dediğinde görevleri çekirdeklere dağıtıp çalıştırıyor ve
  sonuçları birleştiriyor.

Bölümler sırayla işlenebildiği için dask belleğinden büyük verilerle de
çalışabiliyor.

Örneklerde bir milyon sipariş dört CSV dosyasına bölünmüş:
`orders-0.csv` … `orders-3.csv` (her biri 250 000 satır).

## Bir dask tablosu

```python
import dask.dataframe as dd

ddf = dd.read_csv("orders-*.csv")
print(ddf.npartitions)
print(ddf.dtypes)
```

```text
4
order_id         int64
order_time      string
customer_id      int64
city            string
category        string
quantity         int64
unit_price     float64
payment         string
dtype: object
```

- `"orders-*.csv"`: joker karakterle dört dosyanın hepsi; her dosya bir
  bölüm oldu.
- Türler belli ama veri henüz okunmadı: dask yalnızca türleri tahmin etmek
  için dosyaların başına baktı. `print(ddf)` yazsan değerlerin yerinde `...`
  görürsün; dask'ın elinde **veri değil, yapı** var.

## Tembel hesap ve `compute`

Bölüm 3'teki şehir başına ciroyu dask ile yazalım:

```python
revenue = (ddf["quantity"] * ddf["unit_price"]).groupby(ddf["city"]).sum()
print(type(revenue).__name__)
result = revenue.compute()
print((result / 1e6).round(2).sort_values(ascending=False).head(3))
```

```text
Series
city
Istanbul    557.00
Ankara      260.83
Izmir       212.50
dtype: float64
```

Yazım pandas'ınkiyle aynı. Fark şu: `revenue` bir sonuç değil, bir
**tarif**; dask henüz tek bir satır okumadı. `compute()` tarifi çalıştırıyor
ve sonucu sıradan bir pandas nesnesi olarak veriyor. Sayılar Bölüm 3'te elle
bulduklarımızla aynı (İstanbul 557,00 milyon).

Bu tembellik (*lazy evaluation*) dask'ın gücü: işin tamamını görmeden
başlamadığı için gereksiz okumaları atlayabiliyor ve bağımsız adımları aynı
anda çalıştırabiliyor.

`head()` ve `len()` ise hemen çalışıyor: `head` yalnızca ilk bölümün ilk
satırlarını okuyor, `len` bütün dosyaları sayıyor.

## Görev grafiği

`compute()` çağrılınca dask bir görev listesi çıkarıyor: her bölüm için
"oku", "çarp", "grupla ve topla", sonra hepsi için "birleştir".

<figure class="fig">
  <div class="flow">
    <span class="node">Bölümleri oku<br>0 · 1 · 2 · 3</span><span class="arrow">→</span>
    <span class="node">Her bölümde<br>grupla ve topla</span><span class="arrow">→</span>
    <span class="node">Birleştir</span><span class="arrow">→</span>
    <span class="node acc">pandas sonucu</span>
  </div>
  <figcaption>İlk iki adım her bölüm için ayrı ve aynı anda çalışabiliyor; birleştirme hepsi bitince yapılıyor.</figcaption>
</figure>

Bellekteki bir milyon siparişlik `orders` tablosunu sekiz bölüme ayırıp
kategori başına adet toplamı için kaç görev olduğuna bakalım:

```python
ddf8 = dd.from_pandas(orders, npartitions=8)
s = ddf8.groupby("category")["quantity"].sum()
print(len(s.__dask_graph__()))
```

```text
25
```

25 görev. Birbirinden bağımsız olanlar (sekiz bölümün kendi grupları) aynı
anda çalışabiliyor; birleştirme hepsi bitince yapılıyor. Bölüm 3'teki "parçada
özetle, özetleri birleştir" kalıbının aynısı, ama dask kuruyor.

## Bölümler

Her bölüm bellekte bir pandas tablosu olarak işleniyor, bu yüzden bölüm
büyüklüğü önemli:

- `dd.read_csv`: her dosya en az bir bölüm; büyük dosyaları `blocksize=`
  ile parçalıyor.
- `dd.from_pandas(df, npartitions=8)`: bellekteki tabloyu sekize bölüyor.
- `dd.read_parquet`: bu sürümde tek dosyayı tek bölüm olarak okudu;
  `split_row_groups=True` ile her satır grubu ayrı bölüm oldu (10 grup, 10
  bölüm).

Çok küçük bölüm (Bölüm 3'teki çok küçük parça gibi) her bölümün hazırlık
işini çoğaltıyor; çok büyük bölüm belleğe sığmayabiliyor. dask'ın kendi
belgeleri bölüm başına kabaca yüz megabayt öneriyor.

## Birden çok sonucu birlikte hesaplamak

Aynı veriden iki sonuç gerekiyorsa ikisini ayrı ayrı `compute` etmek
dosyaları iki kez okumak demek. `dask.compute` ikisini tek seferde, ortak
adımları paylaşarak hesaplıyor:

```python
import dask

big = ddf[ddf["quantity"] >= 4]
by_category = big.groupby("category")["unit_price"].mean()
count = big.shape[0]
means, n = dask.compute(by_category, count)
print(n)
```

```text
222059
```

## Zamanlayıcılar

Görevleri kimin çalıştıracağına **zamanlayıcı** (*scheduler*) karar
veriyor:

| Zamanlayıcı | Ne yapar | Ne zaman |
|---|---|---|
| `"threads"` | Bir süreçte iş parçacıklarıyla | dask tablolarının varsayılanı; pandas ve NumPy kilidi bırakıyor |
| `"processes"` | Ayrı süreçlerle | Saf Python ağırlıklı iş |
| `"synchronous"` | Tek tek, sırayla | Hata ayıklamak için |

Bu bilgisayarda dört CSV'den şehir başına ciro:

| Yol | Süre |
|---|---|
| pandas (dört dosyayı okuyup birleştir) | 1,41 sn |
| dask, `"threads"` | 0,98 sn |
| dask, `"synchronous"` | 1,45 sn |

Sırayla çalışan dask pandas kadar sürdü; iş parçacıklarıyla 1,4 kat hızlandı.
Burada asıl kazanç hızdan çok **bellek**: dask dört dosyayı hiçbir zaman aynı
anda belleğe almadı.

## `dask.delayed`: herhangi bir fonksiyonu tembel yapmak

dask yalnızca tablolar için değil. `delayed` sıradan bir Python fonksiyonunu
tembel ve paralel hâle getiriyor:

```python
import time
from dask import delayed

def slow_square(x):
    time.sleep(0.2)
    return x * x

parts = [delayed(slow_square)(i) for i in range(8)]
total = delayed(sum)(parts)
print(total.compute())
```

```text
140
```

- `delayed(slow_square)(i)` fonksiyonu çağırmıyor; "çağrılacak" diye
  kaydediyor.
- `delayed(sum)(parts)` sekiz sonucu toplayan son adımı ekliyor.
- `compute()` sekiz çağrıyı aynı anda çalıştırdı: 0,21 saniye. Sırayla
  (`scheduler="synchronous"`) 1,61 saniye sürdü.

## `dask.bag`: kayıt listeleri için

JSON satırları, kayıt dosyaları gibi tabloya uymayan veriler için
`dask.bag` var: bir kayıt listesini bölümlere ayırıp `map`, `filter` gibi
işlemleri paralel yapıyor.

```python
import json
import dask.bag as db

if __name__ == "__main__":
    bag = db.read_text("orders.jsonl").map(json.loads)
    izmir = bag.filter(lambda r: r["city"] == "Izmir").count().compute()
```

**Dikkat:** `dask.bag`'in varsayılan zamanlayıcısı **süreçler**. Bölüm
10'daki kural burada da geçerli: `if __name__ == "__main__":` olmadan bu
kod Windows'ta `RuntimeError` ve `BrokenProcessPool` ile düştü (denendi).

## pandas'tan farkları

dask pandas'ın yazımını taklit ediyor ama her şeyi aynı biçimde yapamıyor.
Bütün veriyi aynı anda görmeyi gerektiren işler zor ya da yaklaşık:

```python
ddf["unit_price"].median().compute()
# NotImplementedError: Dask doesn't implement an exact median in all cases ...
print(ddf["unit_price"].quantile(0.5).compute())
```

```text
449.72
```

Kesin ortanca 449,05; dask'ın `quantile` sonucu 449,72, çünkü yaklaşık
bir yöntem kullanıyor. Bölüm 3'teki tablo burada da geçerli: ortanca
parçalardan kesin bulunamıyor.

Benzer şekilde bütün tabloyu sıralamak (`sort_values`) ya da indeksi
değiştirmek (`set_index`) verinin bölümler arasında yer değiştirmesini
(*shuffle*) gerektirdiği için pahalı.

## Ne zaman dask?

- Veri belleğe sığmıyor ama **pandas yazımıyla** çalışmak istiyorsun.
- Çok sayıda dosya var ve hepsine aynı işlemi uygulayacaksın.
- Elinde paralel çalıştırmak istediğin kendi Python fonksiyonların var
  (`delayed`).

Veri belleğe rahatça sığıyorsa pandas daha basit ve çoğu zaman yeterince
hızlı. İş SQL ile anlatılabiliyorsa DuckDB çoğu zaman daha hızlı. dask ayrıca
birçok bilgisayardan oluşan bir **kümede** de çalışabiliyor; o zaman aynı kod
çekirdekler yerine makinelere dağılıyor. Bu, iki bölüm sonra Spark'la
göreceğimiz dünyanın kapısı.

## Özet

- dask tabloyu pandas bölümlerine ayırıyor, işlemleri görev grafiği olarak
  kaydediyor, `compute()` ile paralel çalıştırıyor.
- `dd.read_csv("orders-*.csv")`: her dosya bir bölüm; yazdırınca yapı
  görünüyor, veri değil.
- `compute()` sonucu pandas nesnesi; `dask.compute(a, b)` iki sonucu ortak
  okumayla hesaplıyor.
- Zamanlayıcılar: `threads` (varsayılan), `processes`, `synchronous`.
- `delayed` herhangi bir fonksiyonu tembel ve paralel yapıyor; `dask.bag`
  kayıt listeleri için, varsayılanı süreçler, `if __name__` şart.
- Kesin ortanca yok, `quantile` yaklaşık; sıralama ve indeks değiştirme
  pahalı.
