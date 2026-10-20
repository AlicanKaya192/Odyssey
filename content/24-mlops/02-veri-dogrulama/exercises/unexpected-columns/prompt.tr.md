Dersteki `check_row(row, schema)` fonksiyonunu yaz ve bir denetim ekle: şemada **olmayan** bir sütun da sorundur. Veriyi gönderen bir sütunun adını değiştirdiyse (`tenure` yerine `tenure_months`) bunu böyle anlarsın.

- Önce şemadaki her sütun için dersteki dört denetim, şemanın sırasıyla: `"<sütun>: missing"`, `"<sütun>: <değer!r> is not allowed"`, `"<sütun>: <değer!r> is not a number"`, `"<sütun>: <değer> is out of range"`.
- Sonra satırdaki her sütun için, satırın sırasıyla: şemada yoksa `"<sütun>: unexpected"`.
- Sorunların listesini döndür.

**Beklenen çıktı:**

```
0 problem(s)
2 problem(s)
  tenure: 99 is out of range
  plan: 'Pro' is not allowed
2 problem(s)
  tenure: missing
  tenure_months: unexpected
3 problem(s)
  tenure: '12' is not a number
  plan: missing
  note: unexpected
```
