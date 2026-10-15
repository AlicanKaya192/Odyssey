`latest_release(tags)` fonksiyonunu yaz. Git etiketlerinin listesini alsın ve **en yeni kararlı sürümün** etiketini döndürsün; hiç yoksa `None`.

- Kararlı sürüm etiketi: `v` ile başlar, ardından noktayla ayrılmış **tam üç parça** gelir ve her parça yalnızca rakamdır (`v1.10.0`). `v2.0.0rc1`, `v1.10`, `nightly` sayılmaz.
- Sürümler **sayı olarak** karşılaştırılır: `v1.10.0`, `v1.9.3`'ten yenidir.

`part.isdigit()` bir metnin yalnızca rakamdan oluşup oluşmadığını söyler.

**Beklenen çıktı:**

```
v1.10.0
None
v0.10.0
```
