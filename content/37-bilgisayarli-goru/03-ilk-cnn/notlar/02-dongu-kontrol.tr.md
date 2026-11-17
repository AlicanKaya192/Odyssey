Eğitim beklenmedik davranıyorsa önce bu listeye bak:

| Belirti | Sık sebep |
|---|---|
| Kayıp hiç düşmüyor | `optimizer.step()` unutulmuş ya da optimizer'a başka modelin parametreleri verilmiş |
| Kayıp düşüyor ama sonra savruluyor | `zero_grad()` unutulmuş: türevler birikiyor |
| Kayıp başta `log(sınıf sayısı)`'ndan çok büyük | Son katmandan sonra softmax konmuş (`CrossEntropyLoss` ham puan ister) |
| Test doğruluğu her ölçümde biraz farklı | `model.eval()` unutulmuş |
| Etiket türü hatası | Etiketler `float`; `CrossEntropyLoss` `int64` ister |

İkinci satırın sebebi PyTorch'un türevleri **üstüne eklemesi**:

```python
import torch

w = torch.tensor([2.0], requires_grad=True)
loss = (w * 3).sum()
loss.backward()
print(w.grad.item())
loss = (w * 3).sum()
loss.backward()
print(w.grad.item())
w.grad.zero_()
print(w.grad.item())
```

```text
3.0
6.0
0.0
```

İkinci `backward` türevi 3'ten 6'ya çıkardı: yeni türev eskisinin üstüne
eklendi. Her yığında `optimizer.zero_grad()` bu birikimi temizliyor. (Bu
davranış bilerek seçilmiş: bellek yetmeyince birkaç küçük yığının türevini
toplayıp tek adım atmak için kullanılıyor.)
