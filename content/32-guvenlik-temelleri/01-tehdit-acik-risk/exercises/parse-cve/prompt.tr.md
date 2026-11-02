`parse_cve(text)` fonksiyonunu yaz. Metin geçerli bir CVE kimliğiyse
`(yil, numara)` demetini (ikisi de `int`), değilse `None` döndürsün.

- Önce baştaki ve sondaki boşlukları at, büyük harfe çevir (`strip`, `upper`).
- `-` ile bölününce tam **üç** parça olmalı ve ilki `"CVE"` olmalı.
- Yıl tam **4** basamak ve en az `1999`; numara en az **4** basamak.
  Basamak denetimi için `isdigit()`.

**Beklenen çıktı:**

```
'CVE-2025-12345' (2025, 12345)
' cve-2019-0042 ' (2019, 42)
'CVE-25-1234' None
'CVE-2024-12a4' None
```
