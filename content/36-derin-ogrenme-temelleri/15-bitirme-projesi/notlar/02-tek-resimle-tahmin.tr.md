Gerçek kullanımda model çoğu zaman tek bir resim alır. Model kümeyle
çalışacak şekilde yazıldığı için tek resme bir küme boyutu eklenir:
`(64,)` → `(1, 64)`. Bunu yapan küçük bir tahmin fonksiyonu:

```python
def predict(net, image):
    net.eval()
    with torch.no_grad():
        logits = net(image.unsqueeze(0))
    return logits.argmax(dim=1).item()


print([predict(fresh, X[i]) for i in test_idx[:8].tolist()])
print(Y[test_idx[:8]].tolist())

fresh.train()
try:
    fresh(X[test_idx[0]].unsqueeze(0))
except ValueError as error:
    print(str(error).split(",")[0])
```

```text
[2, 4, 8, 4, 9, 6, 8, 4]
[2, 4, 8, 4, 9, 6, 8, 7]
Expected more than 1 value per channel when training
```

- İlk sekiz test resminin yedisi doğru; sonuncusu bir 7'yi 4 sandı.
- Fonksiyon `net.eval()`'i kendisi çağırıyor. Çağırmasaydı BatchNorm eğitim
  kipinde kalırdı ve tek resimde hata verirdi: son satır tam bu hata
  (Başlatma ve Normalizasyon bölümünün notu).
- `torch.no_grad()` tahminde türev kaydını kapatır; hem hızlı hem bellek
  dostu.
