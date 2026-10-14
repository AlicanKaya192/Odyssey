`mask_count(text)` dersteki üç deseni (`EMAIL`, `PHONE`, `ORDER`) sırayla
uygulasın ve `[maskelenmiş metin, toplam maskelenen parça sayısı]`
döndürsün. Sayı için `re.subn` kullanılabilir: değiştirilmiş metni ve
değiştirme sayısını birlikte verir.

**Beklenen çıktı:**

```
['Mail [EMAIL], [ORDER]', 2]
```
