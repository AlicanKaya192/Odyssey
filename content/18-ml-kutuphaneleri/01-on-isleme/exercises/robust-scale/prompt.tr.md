`robust_scale(values)` tek sütunlu veriyi **aykırı değere dayanıklı** biçimde
ölçeklesin (`RobustScaler`: medyanı çıkar, çeyrekler arası farka böl) ve 2
basamağa yuvarlı liste döndürsün. Başlangıç kodu `StandardScaler` kullanıyor;
tek bir büyük değer diğerlerini sıkıştırıyor.

**Beklenen çıktı:**

```
[-1.0, -0.5, 0.0, 0.5, 46.0]
```
