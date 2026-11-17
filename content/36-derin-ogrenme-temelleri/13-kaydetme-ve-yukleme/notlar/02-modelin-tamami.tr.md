`torch.save(model)` yalnızca sayıları değil **model nesnesinin kendisini**
kaydeder. Kısa yol gibi görünür ama iki sorunu var:

```python
torch.save(model, "whole.pt")
try:
    torch.load("whole.pt", weights_only=True)
except Exception as error:
    print(type(error).__name__, str(error).split(".")[0])
loaded = torch.load("whole.pt", weights_only=False)
print(type(loaded).__name__, torch.equal(loaded(x), model(x)))
```

```text
UnpicklingError Weights only load failed
Sequential True
```

- Güvenli kipte reddedildi: dosyada `Sequential` ve `Linear` nesneleri var.
  Yalnızca güvenli olmayan kipte (`weights_only=False`) açılabildi; bu
  dosyayı biz kendimiz yazdığımız için burada sorun yok, başkasınınki için
  var.
- Dosya, modelin sınıfına **adıyla** bağlı. Kendi yazdığın bir sınıfı
  (`class TableNet(nn.Module)`) böyle kaydedersen, yükleyen programda aynı
  adlı sınıf aynı modülde bulunmak zorunda; kodu taşıyınca ya da sınıfın
  adını değiştirince dosya açılmaz.
- state_dict bu iki sorundan da kurtarıyor: yalnızca tensörler, güvenli
  kipte açılıyor, sınıfı istediğin gibi düzenleyebilirsin.
