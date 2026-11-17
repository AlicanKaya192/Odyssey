Softmax sınıfları **yarıştırır**: biri artınca ötekiler azalır, toplam
hep 1. Bu, her örneğin tek bir sınıfı olduğu görevler için doğru (bu rakam
ya 3'tür ya 8). Bazı görevlerde ise bir örnek birden çok etikete sahip
olabilir: bir fotoğrafta hem kedi hem köpek olabilir. Buna **çok etiketli**
(multi-label) sınıflandırma denir ve her etiket için ayrı bir sigmoid
kullanılır:

```python
logits = torch.tensor([[2.0, -1.0, 0.5]])
print([round(v, 3) for v in torch.sigmoid(logits)[0].tolist()])
print([round(v, 3) for v in torch.softmax(logits, dim=1)[0].tolist()])
labels = torch.tensor([[1.0, 0.0, 1.0]])
print(round(nn.BCEWithLogitsLoss()(logits, labels).item(), 4))
```

```text
[0.881, 0.269, 0.622]
[0.786, 0.039, 0.175]
0.3048
```

- Sigmoid her etiketi ayrı ayrı değerlendiriyor: birinci ve üçüncü etiket
  0,5'ten büyük, ikisi birden "var". Toplamları 1 değil.
- Softmax aynı puanları yarıştırıyor; üçüncü etiket ikinciden yüksek ama
  birinciyle paylaşmak zorunda.
- Çok etiketli görevin kaybı `BCEWithLogitsLoss`, hedefler 0/1'lerden
  oluşan bir satır.

<figure class="fig">
  <div class="versus">
    <div><h5>Tek etiket (multi-class)</h5>Son katman sınıf sayısı kadar logit, kayıp <code>CrossEntropyLoss</code>, hedef sınıf numarası.</div>
    <div><h5>Çok etiket (multi-label)</h5>Son katman etiket sayısı kadar logit, kayıp <code>BCEWithLogitsLoss</code>, hedef 0/1 satırı.</div>
  </div>
  <figcaption>İki farklı görev, iki farklı kayıp.</figcaption>
</figure>
