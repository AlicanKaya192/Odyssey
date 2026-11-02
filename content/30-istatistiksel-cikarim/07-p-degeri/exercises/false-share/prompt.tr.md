`false_share(n_ideas, share_work, power, alpha)` beklenen sayılarla
hesaplasın: işe yaramayan fikirlerden gelen yanlış alarm
`n_ideas * (1 - share_work) * alpha`, işe yarayanlardan gelen doğru sonuç
`n_ideas * share_work * power`. Anlamlı sonuçlar içinde yanlış alarmların
payını 3 basamakla döndür. Başlangıç kodu bu payın `alpha` olduğunu
varsayıyor; değil.

**Beklenen çıktı:**

```text
0.726
0.36
```
