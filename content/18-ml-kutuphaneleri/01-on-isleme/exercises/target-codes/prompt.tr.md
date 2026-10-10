`target_codes(shops, bought, new_shops)` mağazaları `TargetEncoder(random_state=0)`
ile kodlasın: eğitim mağazaları ve hedefle (`bought`) `fit`, yeni mağazalarla
`transform`. Yeni mağazaların kodlarını 3 basamağa yuvarlı liste olarak
döndürsün. Veriyi `pd.DataFrame({"shop": ...})` olarak ver. Başlangıç kodu
ortalamayı elle hesaplıyor: hiç görülmemiş mağazada `nan` çıkıyor ve az
kayıtlı mağazanın ortalaması düzleştirilmiyor.

**Beklenen çıktı:**

```
[0.651, 0.725, 0.6]
```
