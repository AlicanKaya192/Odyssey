`Version` sınıfını tamamla: `"1.10.2"` gibi metni noktalardan bölüp
`self.parts` demetine çevirsin (`int`), `__eq__` ve `__lt__` bu demetleri
karşılaştırsın, sınıf **`@total_ordering`** ile süslensin. Sonra
`sort_versions(texts)` metinleri sürüm sırasına göre sıralayıp döndürsün:
`"1.2"`, `"1.10"`'dan önce gelir.

**Beklenen çıktı:**

```
['0.9', '1.2', '1.2.1', '1.10']
True
```
