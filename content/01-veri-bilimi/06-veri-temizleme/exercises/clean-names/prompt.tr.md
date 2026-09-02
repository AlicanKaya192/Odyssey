Temizliğin **ilk işi** sütun adları. Onlar düzelmeden hiçbir şey
yazamıyorsun.

**Yapman gerekenler:**

1. `raw` tablosunun bir **kopyasını** al, adı `data` olsun.
2. Sütun adlarındaki boşlukları at ve hepsini küçük harfe çevir.
3. Yeni sütun adlarını liste hâlinde yazdır.
4. `name` sütununun değerlerini liste hâlinde yazdır.

**Beklenen çıktı:**

```
['name', 'city', 'score']
[' Ada ', 'kerem', 'MINA', 'Ada ', 'Deniz', 'efe ', 'Sila']
```

**Neden ilk iş bu:** `" Name "` ile `"name"` farklı iki ad ve ekranda ikisi
de aynı görünüyor. Adları düzeltmeden `data["name"]` yazamıyorsun.

Sütun adları da bir seri gibi davranıyor, `.str` metotları onlarda da
çalışıyor.

**İkinci satır bir sonraki işi gösteriyor:** değerlerde hâlâ boşluk ve
tutarsız harf var. Sırada o var.
