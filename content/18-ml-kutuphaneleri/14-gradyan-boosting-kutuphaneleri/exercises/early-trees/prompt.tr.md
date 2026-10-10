Veri 3750 eğitim satırı; `early_stopping="auto"` 10 000 satırın altında
**kapalı** kalır. `early_trees(rate)` modeli `early_stopping=True` ile kursun
(1000 ağaç sınırı) ve `[kullanılan_ağaç, test_skoru]` döndürsün (`n_iter_`,
skor 3 basamak). Başlangıç kodu 1000 ağacın hepsini eğitiyor.

**Beklenen çıktı:**

```
[48, 0.91]
[25, 0.907]
```
