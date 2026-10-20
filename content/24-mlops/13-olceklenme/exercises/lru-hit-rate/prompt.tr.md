Dersteki LRU önbelleğinin isabet oranını hesaplayan `hit_rate(requests, size)` fonksiyonunu yaz:

- `requests`: sırayla sorulan anahtarlar, `size`: önbelleğin alabileceği kayıt sayısı.
- Anahtar önbellekteyse isabet say ve onu sona al.
- Değilse ekle; önbellek `size`'ı aşarsa en baştakini (en uzun süredir sorulmayanı) çıkar.
- İsabetlerin istek sayısına oranını üç basamağa yuvarlanmış döndür.

**Beklenen çıktı:**

```
0.0
0.2
0.5
```
