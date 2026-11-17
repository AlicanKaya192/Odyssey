Modelin bir kısmı hiç öğrenmiyorsa ilk bakılacak yer, `backward()`'dan sonra
her parametrenin gradyanının dolu olup olmadığıdır. Araya yanlışlıkla
giren bir `.detach()` (ya da `.item()`, NumPy'a geçiş) türev zincirini
koparır:

```python
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.first = nn.Linear(4, 4)
        self.second = nn.Linear(4, 1)

    def forward(self, x):
        h = torch.relu(self.first(x)).detach()
        return self.second(h)


net = Net()
net(torch.randn(3, 4)).sum().backward()
for name, p in net.named_parameters():
    print(name, None if p.grad is None else tuple(p.grad.shape))
```

```text
first.weight None
first.bias None
second.weight (1, 4)
second.bias (1,)
```

- `second` katmanının gradyanı var, `first`'ün yok (`None`): kayıp,
  `detach` noktasının gerisini göremiyor. Program hata vermiyor; ilk katman
  eğitim boyunca başlangıçtaki rastgele hâlinde kalıyor.
- Aynı döküm donmuş katmanları (`requires_grad=False`) bulmak için de
  işe yarar; onlar da `None` gösterir.
- Kural: modelin `forward`'ında `.detach()`, `.item()`, `.numpy()` ancak
  kasıtlıysa bulunur.
