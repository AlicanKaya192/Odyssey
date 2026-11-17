`model.state_dict()` modelin bütün parametrelerini adlarıyla veren bir
sözlük. Ama içindeki tensörler parametrelerin **kopyası değil, kendisi**:

```python
saved = model.state_dict()
copied = copy.deepcopy(model.state_dict())
with torch.no_grad():
    model[0].bias.add_(1.0)
print(torch.equal(saved["0.bias"], model[0].bias))
print(torch.equal(copied["0.bias"], model[0].bias))
print(list(copied.keys()))
```

```text
True
False
['0.weight', '0.bias', '2.weight', '2.bias']
```

- `saved` modelle birlikte değişti: sabiti 1 artırınca sözlükteki değer de
  arttı. Döngüde "en iyi durum" diye bunu saklasaydık, eğitim bitince
  elimizde en iyi değil **son** durum olurdu.
- `copy.deepcopy` tensörlerin gerçek kopyasını alıyor; model değişince
  kopya değişmiyor.
- Anahtarlar katmanların adları: `nn.Sequential`'da sıra numarası
  (`0.weight`), kendi sınıfında özellik adı (`hidden.weight`). Kaydetme
  bölümünde aynı sözlüğü diske yazacağız.
