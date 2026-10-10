`age_groups(ages)` yaşları `pd.cut` ile şu gruplara ayırsın:
sınırlar `[0, 18, 40, 65, 120]`, adlar `["child", "young", "middle",
"senior"]`. Her grubun kişi sayısını **grupların kendi sırasıyla** ve boş
grup da 0 ile görünecek şekilde `{grup: sayı}` döndürsün
(`value_counts(sort=False)`). **Döngü yazma.**

**Beklenen çıktı:**

```
('child', 2)
('young', 2)
('middle', 0)
('senior', 1)
```
