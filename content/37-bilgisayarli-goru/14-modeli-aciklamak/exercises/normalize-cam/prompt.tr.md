`normalize_cam(cam)` haritanın eksi değerlerini sıfırlasın (ReLU), sonra en
büyük değere bölsün ve 2 basamakla liste listesi döndürsün. Her değer 0 ya da
eksiyse bölme yapma, sıfırlardan oluşan haritayı döndür.

**Beklenen çıktı:**

```
[[0.0, 0.0], [0.5, 1.0]]
[[0.0, 0.0], [0.0, 0.0]]
```
