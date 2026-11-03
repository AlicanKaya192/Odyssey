İki fonksiyon yaz:

- `parse_version(text)`: `"2.4.10"` gibi bir sürümü sayılardan oluşan bir
  **demete** çevirsin: `(2, 4, 10)`.
- `needs_patch(installed, fixed)`: kurulu sürüm düzeltilmiş sürümden
  **eskiyse** `True` döndürsün. Karşılaştırmayı demetlerle yap; metin
  karşılaştırması `2.4.10`'u `2.4.9`'dan küçük sanır.

**Beklenen çıktı:**

```
(2, 4, 10)
True
False
False
False
```
