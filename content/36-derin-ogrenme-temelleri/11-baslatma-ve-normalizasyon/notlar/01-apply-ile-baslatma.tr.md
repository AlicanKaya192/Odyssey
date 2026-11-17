Bir modelin bütün katmanlarını aynı kuralla başlatmanın PyTorch'taki
yerleşik yolu `model.apply(fonksiyon)`: fonksiyon modelin her alt modülüne
sırayla uygulanır.

```python
def init_weights(module):
    if isinstance(module, nn.Linear):
        nn.init.kaiming_normal_(module.weight, nonlinearity="relu")
        nn.init.zeros_(module.bias)


torch.manual_seed(0)
model = nn.Sequential(nn.Linear(256, 256), nn.ReLU(), nn.Linear(256, 10))
model.apply(init_weights)
print(model[0].bias.abs().sum().item())
print(round(model[0].weight.std().item(), 2), round(math.sqrt(2 / 256), 2))
```

```text
0.0
0.09 0.09
```

- `isinstance` ile yalnızca `nn.Linear` katmanları seçildi; ReLU'ya
  dokunulmadı (zaten parametresi yok).
- Sabitler sıfırlandı; ağırlıkların standart sapması Kaiming'in formülü
  `sqrt(2 / 256)` ile aynı.
- `apply` iç içe modülleri de dolaşır: kendi sınıfının içindeki
  `nn.Sequential`'ların katmanlarına da ulaşır. Başlatmayı modelin
  `__init__`'inin sonunda `self.apply(...)` ile çağırmak yaygın bir kalıp.
