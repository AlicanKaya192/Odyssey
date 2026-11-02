150'şer kişilik düzen testinde (`make_layout_test()`) Tukey HSD'ye göre
`p < 0.05` olan çiftleri `A C` biçiminde satır satır yazdır (çiftler
`itertools.combinations` sırasıyla). Başlangıç kodu düzeltmesiz
t-testleri kullanıyor ve fazladan çift buluyor.

**Beklenen çıktı:**

```text
A C
B C
```
