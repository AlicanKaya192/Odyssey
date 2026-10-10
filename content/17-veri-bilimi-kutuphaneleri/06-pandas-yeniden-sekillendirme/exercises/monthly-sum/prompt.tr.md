`monthly_sum(records)` `[şehir, ay, satış]` kayıtlarında aynı çift birden fazla
kez geçebiliyor; başlangıç kodundaki `pivot` bu yüzden hata veriyor.
`pivot_table` ile toplasın (`aggfunc="sum"`), kaydı olmayan hücre 0 olsun
(`fill_value=0`) ve sonucu `{şehir: {ay: toplam}}` sözlüğü olarak döndürsün
(`to_dict(orient="index")`). **Döngü yazma.**

**Beklenen çıktı:**

```
{'feb': 0, 'jan': 80}
{'feb': 65, 'jan': 0}
```
