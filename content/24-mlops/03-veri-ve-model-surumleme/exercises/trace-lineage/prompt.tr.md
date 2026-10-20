Soy kayıtları bir sözlük: her ad için `{"from": üst_ad}`; en baştaki verinin `"from"` değeri `None`. `trace(records, start)` fonksiyonunu yaz ve `start`'tan geriye doğru zinciri liste olarak döndür:

- `start` adından başla, listeye ekle ve `"from"` ile bir üste geç.
- `"from"` değeri `None` olunca dur.
- Zincirdeki bir ad `records` içinde **yoksa** listeye `"<ad> (missing)"` ekle ve dur: soyun o halkası kayıp.

**Beklenen çıktı:**

```
model-3
data-v3
data-v2
data-v1
---
model-4
data-v5 (missing)
```
