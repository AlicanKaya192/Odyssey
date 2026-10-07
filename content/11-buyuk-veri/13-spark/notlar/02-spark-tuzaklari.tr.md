Spark kodu çoğu zaman çalışıyor; sorun yavaşlık ya da sürücünün belleği.
Sık yapılan hatalar.

## 1. Büyük sonuca `collect()`

`collect()` bütün sonucu sürücüye getiriyor. Milyarlarca satırda sürücü çöker.
Önce süz ve özetle; büyük sonucu diske yaz (`df.write.parquet(...)`), ya da
yalnızca birkaç satıra bak (`take(10)`, `show()`).

## 2. `groupByKey` ile toplamak

```python
rdd.groupByKey().mapValues(sum)      # her değer ağdan geçer
rdd.reduceByKey(lambda a, b: a + b)  # önce bölümde toplanır
```

İkisi aynı sonucu veriyor ama `reduceByKey` birleştirici kullandığı için
ağdan çok daha az veri gönderiyor (Bölüm 12: bir milyon çift yerine 32).

## 3. İki kez kullanılan RDD'yi önbelleğe almamak

Spark tembel: aynı RDD iki eylemde kullanılırsa tarif iki kez çalışıyor. Bu
bölümdeki örnekte `cache()` ile 6, onsuz 12 bölüm hesabı. Tekrar
kullanacağın, hesaplaması pahalı RDD'leri önbelleğe al; işin bitince bırak.

## 4. Gereksiz shuffle

Her geniş dönüşüm bir shuffle. `distinct`, `sortBy`, `groupBy`'ı gerçekten
gerektiğinde ve olabildiğince az kullan; süzmeyi shuffle'dan **önce** yap.

## 5. Çarpık anahtar

Bir anahtar verinin büyük kısmını taşıyorsa (Bölüm 12'de bir makineye
siparişlerin %66'sı) o bölüm herkesi bekletir. Tuzlama ya da farklı bir
anahtar düşün.

## 6. Çok az ya da çok fazla bölüm

Bölüm sayısı çekirdek sayısından azsa çekirdekler boşta kalır; çok fazlaysa
her bölümün hazırlık işi büyür (Bölüm 3'teki küçük parçalar). Yaygın öneri,
çekirdek sayısının birkaç katı kadar bölüm.

## 7. Eylemi döngüde çağırmak

```python
for city in cities:
    df.filter(f"city == '{city}'").count()   # her turda bütün plan çalışır
```

Tek bir `groupBy("city").count()` yeter.

## 8. Tembelliği unutmak

Bir dönüşüm satırı hata vermedi diye doğru olduğu anlaşılmaz: hata ancak
eylemde, çok sonra çıkabilir. Yazarken küçük bir örnekte sık sık `take(5)`
ile bak.
