`error_counts(log)` fonksiyonunu yaz: `log` her satırı `tarih saat
DÜZEY mesaj` biçiminde olan çok satırlı bir metin. Düzeyi `ERROR` olan
satırların mesajlarını sayıp `{mesaj: adet}` sözlüğü döndürsün. Kalıp
`re.MULTILINE` ile: `^\S+ \S+ ERROR (.+)$`.

**Beklenen çıktı:**

```
{'disk full': 2, 'timeout': 1}
```
