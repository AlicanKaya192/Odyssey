Bir katmanın öğrenmesini istemiyorsak parametrelerinin `requires_grad`'ını
kapatırız. Buna **dondurmak** (freezing) denir; Bilgisayarlı Görü
modülündeki transfer öğrenmede önceden eğitilmiş katmanlar böyle korunuyor.

```python
for p in model.hidden.parameters():
    p.requires_grad = False
trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
total = sum(p.numel() for p in model.parameters())
print(trainable, total)
before_w = model.hidden.weight.clone()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
loss = nn.CrossEntropyLoss()(model(x), y)
loss.backward()
optimizer.step()
print(torch.equal(before_w, model.hidden.weight), model.hidden.weight.grad)
```

```text
51 163
True None
```

- `hidden` katmanının 112 parametresi donduruldu; eğitilecek olan yalnızca
  `out` katmanının 51 parametresi.
- Donmuş katmanın gradyanı hiç hesaplanmadı (`None`) ve `step()` onu
  değiştirmedi.
- Optimizer'a bütün parametreleri vermek zararsız: gradyanı olmayan
  parametreyi atlıyor. İstersen yalnızca eğitilecekleri de verebilirsin:
  `[p for p in model.parameters() if p.requires_grad]`.
