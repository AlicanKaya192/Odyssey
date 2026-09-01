Yanına `report.txt` adında bir dosya konuldu. İçinde bazı satırlar boş.

**Yapman gerekenler:**

1. `report.txt` dosyasını oku.
2. `total` adında bir değişkende **toplam** satır sayısını tut.
3. `filled` adında bir değişkende **boş olmayan** satır sayısını tut.
4. Önce `total`, sonra `filled` yazdır.

**Beklenen çıktı:**

```
5
3
```

Dikkat: bir satır yalnızca boşluk da içeriyor olabilir. `strip()` sonrası
boşsa o satır boş sayılıyor.

> Boşluk kontrolü için `if not line.strip():` yazabilirsin — boş metin
> Python'da `False` sayılıyor.
