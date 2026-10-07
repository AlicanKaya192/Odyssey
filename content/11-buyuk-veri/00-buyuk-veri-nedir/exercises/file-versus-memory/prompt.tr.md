`orders_data.py` (salt okunur sekme) siparişleri üretiyor. 100 000
siparişi CSV'ye yaz, geri oku ve iki boyutu karşılaştır.

**Yapman gerekenler:**

1. `write_orders_csv("orders.csv", 100_000)` ile dosyayı yaz.
2. Dosyayı `pd.read_csv` ile `df` tablosuna oku.
3. Satır sayısını yazdır.
4. Dosyanın diskteki boyutunu (`os.path.getsize`) ve tablonun bellekteki
   boyutunu (`memory_usage(deep=True).sum()`) MB olarak, bir ondalığa
   yuvarlayıp aynı satıra yazdır.
5. Bellekteki boyutun dosya boyutuna oranını iki ondalığa yuvarlayıp
   yazdır.
6. Bellekte en çok yer tutan sütunun adını yazdır. `memory_usage` sonucunda
   indeksin kendi satırı (`"Index"`) da var; önce onu `.drop("Index")` ile
   çıkar, sonra `.idxmax()`.

**Beklenen çıktı:**

```
100000
5.9 9.6
1.62
order_time
```

En pahalı sütun bir metin sütunu. Bir sonraki bölümde sütun sütun
bakacağız.
