Ağırlık çürümesi, kayba ağırlıkların karesini eklemenin (L2 cezası)
gradyan inişindeki karşılığı: her adımda ağırlık kendi büyüklüğüyle orantılı
olarak küçülür. Kaybın hiç gradyan vermediği bir ağırlıkta bunu tek başına
görebiliriz:

```python
w = torch.tensor([1.0], requires_grad=True)
optimizer = torch.optim.SGD([w], lr=0.1, weight_decay=0.1)
for _ in range(3):
    optimizer.zero_grad()
    (w * 0).sum().backward()
    optimizer.step()
    print(round(w.item(), 4))
```

```text
0.99
0.9801
0.9703
```

- Kayıp `w · 0`, yani gradyanı 0. Yine de `w` her adımda `1 − lr · wd =
  0,99` katına iniyor: 0,99, 0,9801, 0,9703.
- Veri bir ağırlığı büyütmeye gerçekten ihtiyaç duymuyorsa çürüme onu
  yavaşça sıfıra götürür. Ezberden gelen büyük, tuhaf ağırlıklar böyle
  törpülenir.
- `Adam`'da `weight_decay` gradyana eklenip Adam'ın ölçeklemesinden
  geçtiği için etkisi bozuluyor; `AdamW` çürümeyi ayrı uygular. Adam
  kullanırken çürüme istiyorsan `AdamW` seç (derste de öyle yaptık).
