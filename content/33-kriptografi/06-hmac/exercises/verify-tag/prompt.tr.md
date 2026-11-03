`make_tag` hazır. `verify_tag(key_hex, message, tag)` beklenen etiketi
yeniden hesaplasın ve verilen `tag` ile **sabit süreli** karşılaştırsın
(`hmac.compare_digest`); eşitse `True`, değilse `False` döndürsün. `==`
kullanma.

**Beklenen çıktı:**

```
True
False
False
```
