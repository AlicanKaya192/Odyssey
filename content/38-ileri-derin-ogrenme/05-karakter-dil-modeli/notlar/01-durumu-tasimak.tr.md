Üretirken bütün metni her adımda yeniden okutmak yerine LSTM'in durumunu
taşıdık. İkisinin aynı sonucu verdiğini görelim: aşağıdaki kod dersteki
eğitilmiş modeli kullanıyor; "the cat sat"i bir kez bütün olarak, bir kez de
ilk 5 karakterden sonra karakter karakter okutuyor.

```python
model.eval()
with torch.no_grad():
    ids = torch.tensor([[index[c] for c in "the cat sat"]])
    full, _ = model(ids)
    logits, state = model(ids[:, :5])
    for t in range(5, ids.shape[1]):
        logits, state = model(ids[:, t:t + 1], state)
print(ids.shape[1], torch.allclose(full[0, -1], logits[0, -1], atol=1e-5))
```

```text
11 True
```

Son karakterin logitleri iki yolda aynı. LSTM'in bütün geçmişi `(h, c)`
durumunda; durumu veren, geçmişi yeniden vermiş olur.

## Eğitimde durum: kesilmiş geri yayılım

Çok uzun bir metinde (bir kitap) pencereler arka arkaya gelir ve durumu bir
pencereden ötekine taşımak ağın daha uzun bir geçmişi görmesini sağlar.
Ama türevin bütün kitap boyunca geri yürümesi bellek ve süre açısından
imkânsız. Çözüm **kesilmiş zamanda geri yayılım** (truncated BPTT):

```text
state = None
for x, y in windows_in_order:
    logits, state = model(x, state)
    state = tuple(s.detach() for s in state)
    ...  # kayıp, backward, step
```

`detach()` durumun **değerini** sonraki pencereye taşır ama türev bağını
keser: türev yalnızca o pencerenin içinde geri yürür. `detach` unutulursa
ikinci pencerenin `backward()`'u birinci pencerenin zaten serbest bırakılmış
hesap grafiğine ulaşmaya çalışır ve "Trying to backward through the graph a
second time" hatası verir.
