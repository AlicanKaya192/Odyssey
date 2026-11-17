Optimizer'ın öğrenme oranı sabit bir sayı değil; `param_groups` listesinde
duran, eğitim sırasında değiştirilebilen bir ayar. Ayrıca farklı
katmanlara farklı öğrenme oranı verilebilir:

```python
model = nn.Sequential(nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, 10))
optimizer = torch.optim.SGD([
    {"params": model[0].parameters(), "lr": 0.01},
    {"params": model[2].parameters()},
], lr=0.1)
print([group["lr"] for group in optimizer.param_groups])
for group in optimizer.param_groups:
    group["lr"] = group["lr"] / 2
print([group["lr"] for group in optimizer.param_groups])
```

```text
[0.01, 0.1]
[0.005, 0.05]
```

- Her grup bir sözlük: `params` ve isteğe bağlı ayarlar. Ayarı yazılmayan
  grup, optimizer'a verilen varsayılanı (`lr=0.1`) alıyor.
- Döngüyle her grubun `lr`'sini değiştirmek, eğitim sırasında öğrenme
  oranını düşürmenin en yalın yolu. Öğrenme Oranı Planlama bölümündeki
  zamanlayıcılar içeride tam olarak bunu yapıyor.
- Farklı katmanlara farklı oran, transfer öğrenmede sık kullanılıyor:
  önceden eğitilmiş katmanlara küçük, yeni katmana büyük öğrenme oranı.
