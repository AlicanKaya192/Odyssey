Bu sayfadaki her tuzak bu makinede denendi.

## 1. `ParquetWriter`'ı kapatmamak

```python
writer.write_table(table)
pd.read_parquet("orders.parquet")
# ArrowInvalid: ... Parquet magic bytes not found in footer
```

Altbilgi `close()` ile yazılıyor. Döngüden sonra `writer.close()`'u unutma.

## 2. Parçalar arasında şema farkı

Bir parçada tam sayı, sonrakinde ondalıklı gelen sütun:

```text
ValueError: Table schema does not match schema used to create file
```

Türleri `read_csv`'ye `dtype=` ile sabit ver; her parça aynı türde gelsin.

## 3. Şemayı zorlarken veri kaybetmek

`pa.Table.from_pandas(b, schema=ilk_sema, safe=False)` farklı türü ilk
şemaya **zorluyor**. Ondalıklı 1,5 tam sayı şemasına zorlanınca sessizce 1
oldu. `safe=False` kullanma; türleri baştan doğru ver.

## 4. Sırasız veride `filters=` beklemek

`filters=` yalnızca istatistikleri koşulla çakışmayan grupları atlıyor.
Şehirler her grupta karışıksa `city == "Izmir"` hiçbir grubu atlayamıyor;
okuma yine bütün dosya. Sık süzdüğün sütuna göre sıralı yaz.

## 5. Sıralamanın bedelini unutmak

Şehre göre sıralanınca dosya 26,0 MB'tan 31,7 MB'a büyüdü: önceden sıralı
olan zaman ve sipariş numarası artık karışık. Bir sütuna göre sıralamak
başka bir sütunun düzenini bozabiliyor.

## 6. Satır grubunu çok küçük seçmek

1 000 satırlık gruplarla okuma, 100 000 satırlık gruplardan yaklaşık üç kat
yavaş (0,121 sn'ye karşı 0,037 sn).

## 7. `filters=` her kurulumda yok

`filters=` arkada `pyarrow.dataset` modülünü kullanıyor. Bu modül
yüklenemezse şu hata geliyor:

```text
ValueError: the 'filters' keyword is not supported when the pyarrow.dataset
module is not available
```

Bu durumda atlamayı elle yap: `pq.ParquetFile` ile istatistiklere bak,
uygun grupları `read_row_group` ile oku (bölümdeki Aralık örneği).

## 8. İndeksi istemeden dosyaya koymak

`pa.Table.from_pandas(chunk)` parçanın indeksini de bir sütun olarak
ekleyebiliyor. Parça parça yazarken `preserve_index=False`.
