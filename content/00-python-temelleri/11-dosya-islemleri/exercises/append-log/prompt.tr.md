`"w"` ile `"a"` arasındaki farkı kendi gözünle göreceksin.

**Yapman gerekenler:**

1. `log.txt` dosyasını **sıfırdan** açıp içine `start` satırını yaz.
2. Aynı dosyayı **sona ekleme** kipiyle açıp `step one` satırını ekle.
3. Yine sona ekleme kipiyle `step two` satırını ekle.
4. Dosyayı oku, satırları `entries` adında bir listeye al.
5. Önce satır sayısını, sonra listeyi yazdır.

**Beklenen çıktı:**

```
3
['start', 'step one', 'step two']
```

İkinci ve üçüncü adımda `"w"` kullanırsan önceki satırlar silinir ve sonuçta
tek satır kalır. Fark tam olarak burada.

> Sona ekleme kipi `"a"`.
