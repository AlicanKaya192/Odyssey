Kayıp bir anda `nan` ya da `inf` olursa eğitimin geri kalanı çöpe gider:
`nan` dokunduğu her sayıyı `nan` yapar. En sık neden, sıfırın logaritması:

```python
probs = torch.tensor([[1.0, 0.0], [0.5, 0.5]], requires_grad=True)
target = torch.tensor([1, 0])
loss = -probs[torch.arange(2), target].log().mean()
loss.backward()
print(loss.item(), torch.isfinite(probs.grad).all().item())

logits = torch.tensor([[10.0, -10.0]], requires_grad=True)
loss = nn.functional.cross_entropy(logits, torch.tensor([1]))
loss.backward()
print(round(loss.item(), 1), torch.isfinite(logits.grad).all().item())
```

```text
inf False
20.0 True
```

- Olasılıklardan elle kayıp hesaplamak, doğru sınıfa tam 0 verilince
  `log 0 = −inf` üretti ve gradyan bozuldu.
- `cross_entropy` aynı "çok emin ve yanlış" durumu logits'ten hesaplayınca
  sonlu ve büyük bir kayıp verdi; gradyan da sonlu. Logaritmayı softmax'la
  birlikte, taşmayacak biçimde kendisi hesaplıyor. Elle `log(softmax(...))`
  yazmak yerine `cross_entropy` ya da `log_softmax` kullanmanın nedeni bu.
- Eğitim döngüsüne tek satırlık bir bekçi konabilir:
  `if not torch.isfinite(loss): raise ValueError(...)`. Böylece hata,
  `nan`'ın ilk çıktığı adımda yakalanır.
- Öteki nedenler: çok büyük öğrenme oranı (ıraksama), ölçeklenmemiş girdi,
  sıfıra bölme. Gradyan kırpma ve normalizasyon bölümleri bunlara karşı.
