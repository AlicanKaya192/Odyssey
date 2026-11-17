Model eğitilmiş, `quantize` hazır. Her `nn.Linear` katmanının ağırlığını
nicemle, `(q, scale)` çiftini `stored` listesine ekle ve ağırlığı geri
açılmış değerle (`q.float() * scale`) değiştir; hepsini `torch.no_grad()`
içinde yap. Son iki satır kaç katmanın saklandığını, türünü ve doğruluğun
yakın kalıp kalmadığını yazıyor.

**Beklenen çıktı:**

```
3 torch.int8
True
```
