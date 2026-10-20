Bir ML sisteminde üç şey değişebilir: kod, veri ve model. Her sürüm bir sözlükle yazılıyor:

- `{"code": "c1", "data": "d1", "model": "m1"}`

Değerler, o parçanın kimliği. Kimlik değiştiyse parça değişmiştir.

`review(old, new)` fonksiyonunu yaz. Eski ve yeni sürümü karşılaştırıp şunu döndürsün:

- Hiçbiri değişmediyse: `"nothing"`
- Kod ya da veri değişti, model aynıysa: `"retrain"` (model eskidi)
- Model değişti, kod ve veri aynıysa: `"unknown model"` (bu model nereden geldi?)
- Model de, kod ya da veri de değiştiyse: `"ok"`

**Beklenen çıktı:**

```
nothing
retrain
unknown model
ok
```
