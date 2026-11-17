Bazen bir hesabın grafiğe girmesini istemeyiz: tahmin yaparken, bir
değeri yazdırırken ya da NumPy'ye geçerken. İki araç var:

```python
w = torch.tensor(3.0, requires_grad=True)
with torch.no_grad():
    doubled = w * 2
print(doubled.requires_grad, (w * 2).requires_grad)
d = w.detach()
print(d.requires_grad, d.item())
try:
    w.numpy()
except RuntimeError as error:
    print(str(error).split(".")[0])
print(w.detach().numpy())
```

```text
False True
False 3.0
Can't call numpy() on Tensor that requires grad
3.0
```

- `torch.no_grad()` bloğunun içindeki hiçbir işlem kaydedilmiyor. Tahmin
  ve değerlendirme kodunda kullanılır; bellek ve zaman kazandırır.
- `detach()` aynı veriyi gösteren ama grafikten kopmuş bir tensör veriyor.
- Gradyan isteyen bir tensör doğrudan NumPy'ye çevrilemiyor; hata mesajı
  çözümü de söylüyor: önce `detach()`.

Kayıp değerini kaydederken `loss.item()` yaz, `loss`'un kendisini bir
listede biriktirme: tensör grafiği de yanında tutar ve bellek boşuna
büyür.
