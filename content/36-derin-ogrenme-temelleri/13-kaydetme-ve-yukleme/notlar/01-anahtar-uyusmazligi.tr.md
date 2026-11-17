`load_state_dict` dosyadaki anahtarlarla modelin anahtarlarını tek tek
eşleştirir. Model değişmişse (bir katman eklendi, bir katman genişledi)
hangi anahtarın neden tutmadığını söyleyerek hata verir:

```python
saved = torch.load("model.pt", weights_only=True)
deeper = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 8),
                       nn.ReLU(), nn.Linear(8, 3))
try:
    deeper.load_state_dict(saved)
except RuntimeError as error:
    for line in str(error).splitlines()[1:]:
        print(line.strip().split(":")[0])

longer = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 3),
                       nn.ReLU(), nn.Linear(3, 3))
result = longer.load_state_dict(saved, strict=False)
print(result.missing_keys)
```

```text
Missing key(s) in state_dict
size mismatch for 2.weight
size mismatch for 2.bias
['4.weight', '4.bias']
```

- Derin modelde `4.weight` ve `4.bias` dosyada yok (**missing**); `2.weight`
  dosyada `(3, 8)`, modelde `(8, 8)` (**size mismatch**).
- `strict=False` eksik ve fazla anahtarları hata yerine **rapor eder**; var
  olanları yükler. Önceden eğitilmiş bir gövdeye yeni bir çıkış katmanı
  eklerken işe yarar (ileri modüldeki aktarımlı öğrenme).
- `strict=False` şekil uyuşmazlığını bağışlamaz; o yine hatadır.
- GPU'da kaydedilmiş bir dosyayı GPU'suz bilgisayarda açmak için
  `torch.load(yol, map_location="cpu", weights_only=True)`.
