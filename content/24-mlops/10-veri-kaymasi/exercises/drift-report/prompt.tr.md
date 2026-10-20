Dersteki PSI'yi birkaç sütuna uygulayan `drift_report(reference, current, columns, bins)` fonksiyonunu yaz. Satırlar sözlük:

- Her sütun için referansın değerlerini sırala; sınırlar `ordered[len(ordered) * i // bins]`, `i` 1'den `bins - 1`'e.
- Kutuyu `bisect.bisect_left` ile bul; payları en az `0.0001` yap.
- PSI'yi hesapla ve `[sütun, PSI (üç basamak), etiket]` ekle. Etiket: `0.1`'in altı `"stable"`, `0.25`'e kadar `"moderate"`, üstü `"large"`.
- Sütunların sırası korunsun.

**Beklenen çıktı:**

```
['fee', 2.892, 'large']
['calls', 0.0, 'stable']
```
