Gradyanı bulduktan sonra parametreyi kaybı azaltacak yöne kaydırırız:
`w ← w − lr · gradyan`. Bunu doğrudan yazmak hata verir:

```python
w = torch.tensor(5.0, requires_grad=True)
loss = (w - 2) ** 2
loss.backward()
try:
    w -= 0.1 * w.grad
except RuntimeError as error:
    print("in-place" in str(error))
with torch.no_grad():
    w -= 0.1 * w.grad
print(round(w.item(), 2), w.grad.item())
```

```text
True
4.4 6.0
```

- `w -= ...` yerinde bir işlem. PyTorch, gradyan isteyen bir yaprağın
  yerinde değiştirilmesine izin vermiyor; bu güncelleme kaydedilirse bir
  sonraki türev bozulur.
- Güncellemeyi `torch.no_grad()` içinde yapınca iş tamam: `5 − 0,1 · 6 =
  4,4`. Kayıp `(w − 2)²`'nin türevi `2(w − 2) = 6`.
- `optimizer.step()` içeride tam olarak bunu yapıyor. Bir sonraki bölümde
  bu güncellemeyi döngüde tekrarlayıp bir modeli eğiteceğiz.
