Ham bir tablo geldi ve dört ayrı sorunu var. Temizlik bölümünün
sırasını hatırla: **adlar → metin → tip.**

**Yapman gerekenler:**

1. Ham veriyi bozmamak için bir **kopya** al.
2. Sütun adlarındaki boşlukları at ve küçük harfe çevir.
3. `name` sütunundaki baştaki-sondaki boşlukları at.
4. `city` sütununu boşluklardan temizle ve baş harfleri büyük olacak
   şekilde tekleştir.
5. `score` sütununu sayıya çevir.
6. Sırayla yazdır: sütun adları listesi, tipler listesi, şehir sayımı
   **sözlük olarak**, ve not ortalaması (iki ondalık).

**Beklenen çıktı:**

```
['name', 'city', 'score']
['str', 'str', 'int64']
{'Ankara': 3, 'Izmir': 2, 'Bursa': 1}
79.83
```

**Dikkat:** temizlemeden önce `"ankara"`, `"ANKARA"` ve `"Ankara "` üç ayrı
grup sayılıyordu. `value_counts()` çıktısına bak — şimdi üçü tek grup.

`score` sütunu metin geldiği için ortalama alınamıyordu; `to_numeric`
olmadan son satır hata verirdi.

`copy()` alışkanlığı: üç adım sonra bir hata fark ettiğinde ham veriye
dönebilmen gerekiyor.
