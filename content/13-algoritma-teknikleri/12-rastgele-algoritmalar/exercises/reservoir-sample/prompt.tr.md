`reservoir_sample(stream, k, seed)` fonksiyonunu yaz: akıştan `k` öğelik
eşit olasılıklı örnek döndürsün; akış `k`'dan kısaysa hepsi. Üreteç
`rng = random.Random(seed)`.

İlk `k` öğeyi ekle; sonra `i`. öğede (0'dan) `j = rng.randint(0, i)`,
`j < k` ise `sample[j]` yerine yeni öğe. Akışı listeye çevirme: tek geçiş.

**Beklenen çıktı:**

```
[37, 55, 2, 97, 77]
[0, 1, 2]
['e', 'b', 'j']
```
