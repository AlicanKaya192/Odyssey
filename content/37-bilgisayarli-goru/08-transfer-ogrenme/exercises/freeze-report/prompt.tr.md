`freeze_report(num_classes)` `models.resnet18(weights=None)` kursun, bütün
parametreleri dondursun, **sonra** `fc`'yi `num_classes` çıkışlı yeni bir
`Linear` ile değiştirsin ve `[eğitilecek parametre sayısı, donmuş parametre
sayısı]` döndürsün.

**Beklenen çıktı:**

```
[1026, 11176512]
[5130, 11176512]
```
