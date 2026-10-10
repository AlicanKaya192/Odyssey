`monthly_totals(dates, amounts)` tarih indeksli bir seri kursun
(`pd.Series(amounts, index=pd.to_datetime(dates))`), `resample("ME").sum()`
ile aylık toplasın ve `{"YYYY-MM": toplam}` döndürsün. Arada kaydı olmayan ay
da 0 ile yer almalı (resample bunu kendisi yapar). Anahtarlar için
`index.strftime("%Y-%m")`. **Döngü yazma.**

**Beklenen çıktı:**

```
('2026-01', 150)
('2026-02', 0)
('2026-03', 70)
```
