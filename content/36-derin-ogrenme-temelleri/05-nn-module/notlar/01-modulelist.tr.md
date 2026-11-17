Katman sayısı değişken olan bir ağ yazarken katmanları bir listeye koymak
akla gelir. Düz Python listesi **çalışır gibi görünür** ama sessizce
bozuktur:

```python
class ListNet(nn.Module):
    def __init__(self, sizes, use_module_list):
        super().__init__()
        layers = [nn.Linear(a, b) for a, b in zip(sizes, sizes[1:])]
        self.layers = nn.ModuleList(layers) if use_module_list else layers

    def forward(self, x):
        for layer in self.layers:
            x = torch.relu(layer(x))
        return x


plain = ListNet([6, 8, 8, 3], use_module_list=False)
proper = ListNet([6, 8, 8, 3], use_module_list=True)
print(plain(x).shape, len(list(plain.parameters())))
print(proper(x).shape, len(list(proper.parameters())))
```

```text
torch.Size([600, 3]) 0
torch.Size([600, 3]) 6
```

- İki model de çıktı veriyor, şekil aynı. Ama düz listedeki katmanlar
  modele kaydedilmemiş: `parameters()` **boş**.
- Bu modeli eğitmeye kalkınca optimizer'a hiç parametre gitmez. PyTorch
  bunu fark eder ve `optimizer got an empty parameter list` hatası verir;
  ama bir kısmı listede bir kısmı `self.` ile atanmış bir modelde hata
  bile çıkmaz, listedekiler hiç öğrenmez.
- Çözüm `nn.ModuleList` (sözlük için `nn.ModuleDict`): Python listesi gibi
  kullanılır, içindekileri modele kaydeder.
