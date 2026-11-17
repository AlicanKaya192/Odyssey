Momentum ve Adam'ın "hız" ve "ortalama" dediğimiz değerleri bir yerde
saklanıyor: optimizer'ın `state` sözlüğünde, her parametre için ayrı ayrı.
Tek bir adım atıp ne biriktirdiklerine bakalım:

```python
for name, make in [("SGD", lambda p: torch.optim.SGD(p, lr=0.1)),
                   ("momentum", lambda p: torch.optim.SGD(p, lr=0.1, momentum=0.9)),
                   ("Adam", lambda p: torch.optim.Adam(p, lr=0.1))]:
    w = torch.zeros(1000, requires_grad=True)
    optimizer = make([w])
    (w - 1).pow(2).sum().backward()
    optimizer.step()
    state = optimizer.state[w]
    print(name, sorted(state), sum(v.numel() for v in state.values()))
```

```text
SGD [] 0
momentum ['momentum_buffer'] 1000
Adam ['exp_avg', 'exp_avg_sq', 'step'] 2001
```

- Düz SGD hiçbir şey saklamıyor.
- Momentum her parametre için bir hız (`momentum_buffer`): 1000 parametre,
  1000 sayı daha.
- Adam iki ortalama saklıyor (`exp_avg`, `exp_avg_sq`) ve bir adım sayacı
  (`step`): parametre sayısının iki katı kadar ek bellek.

Küçük modellerde fark etmez. Milyarlarca parametreli bir modelde ise Adam'ın
durumu modelin kendisinden büyük yer kaplar; büyük modellerin bellek
hesabında optimizer durumu da sayılır. Modeli kaydederken eğitime kaldığın
yerden devam etmek istiyorsan bu durum da kaydedilir (Kaydetme bölümü).
