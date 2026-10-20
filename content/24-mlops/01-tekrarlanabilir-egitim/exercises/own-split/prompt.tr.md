`train_test_split`'in yaptığını kendin yaz: `split(items, test_share, seed)`.

- `items` listesinin bir **kopyasını** al; asıl listeyi değiştirme.
- Kopyayı `random.Random(seed)` ile kurduğun üreteçle karıştır (`shuffle`).
- Test öğelerinin sayısı `round(len(items) * test_share)`.
- Karışık listenin **ilk** bu kadar öğesi test, geri kalanı eğitim.
- `(train, test)` döndür.

Aynı tohum her seferinde aynı bölmeyi vermeli.

**Beklenen çıktı:**

```
test: ['C7', 'C9', 'C10']
again: ['C7', 'C9', 'C10']
other seed: ['C6', 'C10', 'C4']
original: ['C1', 'C2', 'C3']
```
