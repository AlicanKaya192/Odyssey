`distances(points)` her noktanın her noktaya Öklid uzaklığını 2 basamağa
yuvarlı bir matris (iç içe liste) olarak döndürsün. **Döngü yasak:**
`points[:, None, :] - points[None, :, :]` ile farkları al, karelerini son
eksende topla, karekök.

**Beklenen çıktı:**

```
[0.0, 5.0, 10.0]
[5.0, 0.0, 5.0]
[10.0, 5.0, 0.0]
```
