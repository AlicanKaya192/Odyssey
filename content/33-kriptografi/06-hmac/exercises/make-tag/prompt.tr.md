`make_tag(key_hex, message)` anahtarı (`bytes.fromhex`) ve mesajı
(`encode()`) alıp HMAC-SHA256 etiketini onaltılık metin olarak döndürsün.
`hmac.new(key, message_bytes, hashlib.sha256).hexdigest()`.

**Beklenen çıktı:**

```
dd4da5ef5798f927
64
True
```
