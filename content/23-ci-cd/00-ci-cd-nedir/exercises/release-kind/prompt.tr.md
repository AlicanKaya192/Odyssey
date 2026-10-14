Bir ekibin hattında üç şey kendiliğinden olabilir ya da olmayabilir: testler, paketleme ve yayın.

`release_kind(tests_auto, package_auto, release_auto)` fonksiyonunu yaz. Üç değer de `True` ya da `False`:

- Testler kendiliğinden değilse: `"manual"`
- Testler kendiliğinden, paketleme değilse: `"continuous integration"`
- Paketleme de kendiliğinden, yayın değilse: `"continuous delivery"`
- Üçü de kendiliğindense: `"continuous deployment"`

**Beklenen çıktı:**

```
manual
continuous integration
continuous delivery
continuous deployment
```
