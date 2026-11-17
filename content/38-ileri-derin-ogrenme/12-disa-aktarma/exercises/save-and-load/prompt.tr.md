Dışa aktarılmış `ep`'yi `torch.export.save` ile `model.pt2` dosyasına kaydet,
`torch.export.load` ile geri yükle ve `.module()` ile çağrılabilir yap.
Son satır şekli ve özgün modelle aynı sonucu verip vermediğini yazıyor.

**Beklenen çıktı:**

```
torch.Size([4, 2]) True
```
