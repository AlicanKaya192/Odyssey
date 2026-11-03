Üst alan, alt alanın anahtarının SHA-256 özetini (onaltılık metin)
yayımlıyor. `key_ok(presented, published)` sunulan anahtarın özetini
hesaplayıp yayımlananla **sabit süreli** karşılaştırsın
(`hmac.compare_digest`) ve `True`/`False` döndürsün.

**Beklenen çıktı:**

```
True
False
```
