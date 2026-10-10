`store_panels(hours, sales, stores, order)` `sns.relplot` ile her mağazaya bir
panel açsın (`col="store"`, `col_order=order`, `height=2`). Panel başlıkları
yalnızca mağaza adı olsun (`set_titles("{col_name}")`). `panels.png` olarak
kaydedip şekli kapatsın ve `{"shape": [satır, sütun], "titles": [...]}`
döndürsün. Başlangıç kodunda başlıklar `store = Izmir` biçiminde.

**Beklenen çıktı:**

```
[1, 2]
['Izmir', 'Bursa']
```
