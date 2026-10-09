Yanında `sales.csv` var; sütunları `date`, `customer`, `city`, `amount`. Bazı şehirler virgül içeriyor (`"London, UK"`).

`filter_rows(src, dst, column, minimum)` fonksiyonunu yaz: `src`'deki
satırlardan `column` değeri (`float`) `minimum`'a eşit ya da büyük olanları,
aynı başlıkla `dst`'ye yazsın (`DictReader` + `DictWriter`,
`reader.fieldnames`) ve kaç satır yazdığını döndürsün.

**Beklenen çıktı:**

```
2
date,customer,city,amount
2026-03-01,Ada,"London, UK",120.50
2026-03-02,Grace,"New York, US",200.25
```
