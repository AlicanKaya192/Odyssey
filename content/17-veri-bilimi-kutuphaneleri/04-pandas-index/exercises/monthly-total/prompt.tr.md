`monthly_total(jan, feb)` iki ayın şehir → satış sözlüklerini alıyor. İkisini
`pd.Series`'e çevirip **etiketle** toplasın; bir ayda olmayan şehir 0 sayılsın
(`add(..., fill_value=0)`). Sonucu `{şehir: int}` sözlüğü olarak döndürsün.
Başlangıç kodu `.values` ile sırayla topluyor.

**Beklenen çıktı:**

```
Ankara 220
Bursa 50
Izmir 170
Konya 40
```
