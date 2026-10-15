`image_tags(image, ref, sha)` fonksiyonunu yaz; imajın alacağı tam adların listesini döndürsün, bu sırayla:

- Her zaman `image:` + SHA'nın ilk 7 karakteri.
- `ref` `"refs/heads/main"` ise `image:latest`.
- `ref` `"refs/tags/v"` ile başlıyorsa: `v`'den sonraki sürüm (`image:2.3.1`). Sürümde harf **yoksa** ayrıca kısa hâlleri: `image:2.3` ve `image:2`. Ön sürümde (`3.0.0rc1`) kısa hâl verilmez.

Bir metinde harf olup olmadığını `any(char.isalpha() for char in version)` söyler.

**Beklenen çıktı:**

```
refs/heads/main
  ghcr.io/ada/shop:9c1e4b7
  ghcr.io/ada/shop:latest
refs/heads/cart
  ghcr.io/ada/shop:9c1e4b7
refs/tags/v2.3.1
  ghcr.io/ada/shop:9c1e4b7
  ghcr.io/ada/shop:2.3.1
  ghcr.io/ada/shop:2.3
  ghcr.io/ada/shop:2
refs/tags/v3.0.0rc1
  ghcr.io/ada/shop:9c1e4b7
  ghcr.io/ada/shop:3.0.0rc1
```
