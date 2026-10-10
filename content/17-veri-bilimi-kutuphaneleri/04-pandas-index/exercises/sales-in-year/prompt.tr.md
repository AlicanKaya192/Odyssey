`sales_in_year(rows, year)` `[şehir, yıl, satış]` satırlarından
`["city", "year"]` MultiIndex'li bir tablo kursun ve verilen yılın bütün
şehirlerdeki satışlarını `{şehir: satış}` olarak döndürsün. Başlangıç kodu
`loc[year]` yazıyor; ama `loc` dış düzeye (şehre) bakar. İç düzey için `xs`.

**Beklenen çıktı:**

```
{'Ankara': 110, 'Bursa': 65, 'Izmir': 95}
```
