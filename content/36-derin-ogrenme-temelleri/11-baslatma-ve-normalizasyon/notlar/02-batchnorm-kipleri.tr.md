BatchNorm eğitimde **kümenin** istatistiğini kullanır. Tek örneklik bir
kümenin standart sapması olmadığı için eğitim kipinde hata verir;
değerlendirme kipinde kayıtlı ortalamaları kullanır ve çalışır:

```python
bn = nn.BatchNorm1d(2)
one = torch.tensor([[1.0, 2.0]])
try:
    bn(one)
except ValueError as error:
    print(str(error).split(",")[0])
bn.eval()
print([round(v, 3) for v in bn(one)[0].tolist()])
```

```text
Expected more than 1 value per channel when training
[1.0, 2.0]
```

- Yeni kurulan katmanın kayıtlı ortalaması 0, varyansı 1; `eval()`'de
  girdi neredeyse olduğu gibi geçti.
- Bu yüzden BatchNorm'lu bir modelle tahmin yaparken `model.eval()`
  unutulursa iki sorun çıkar: tek örnekte hata, birden çok örnekte ise
  sonuç kümedeki **öteki örneklere bağlı** olur (aynı resim farklı
  kümelerde farklı tahmin alır).
- Eğitimde çok küçük kümeler (2–4 örnek) de BatchNorm'u kararsız yapar;
  küme büyüklüğü küçük kalacaksa LayerNorm düşünülür.
