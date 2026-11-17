Modelin son katmanına softmax koyup çıktısını `CrossEntropyLoss`'a vermek
hata vermez; neden kötü olduğu kaybın kendisinden görülüyor. Doğru sınıfa
çok emin, **kusursuz** bir model düşünelim:

```python
perfect = torch.tensor([[10.0, 0.0, 0.0]])
target = torch.tensor([0])
loss_fn = nn.CrossEntropyLoss()
print(round(loss_fn(perfect, target).item(), 4))
print(round(loss_fn(torch.softmax(perfect, dim=1), target).item(), 4))
print(round(loss_fn(torch.tensor([[1.0, 0.0, 0.0]]), target).item(), 4))
```

```text
0.0001
0.5515
0.5514
```

- Logits verilince kusursuz modelin kaybı neredeyse 0.
- Olasılıklar verilince kayıp 0,55'in altına inemiyor: kayıp
  fonksiyonu olasılıkları yeniden logit sanıp ikinci kez softmax
  uyguluyor. 0 ile 1 arasına sıkışmış "logitler" en fazla 1 fark
  edebiliyor; üçüncü satır, `[1, 0, 0]`'ın kaybının da neredeyse aynı
  olduğunu gösteriyor.
- Sonuç: model ne kadar iyileşirse iyileşsin kayıp neredeyse değişmiyor,
  gradyanlar küçük kalıyor ve öğrenme yavaşlıyor.

Belirti: eğitim kaybı belli bir değerin altına bir türlü inmiyorsa son
katmanda softmax olup olmadığına bak.
