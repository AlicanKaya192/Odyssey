`cache_key(tool, runner_os, requirements)` fonksiyonunu yaz. `"pip-Linux-1a2b3c4d"` biçiminde bir anahtar döndürsün: araç, işletim sistemi ve içeriğin SHA-256 özetinin ilk 8 karakteri.

Bir şart daha: yalnızca **satır sırası** ya da **boş satırlar** farklıysa anahtar değişmesin. Bunun için özetten önce:

- Metni satırlara böl, her satırın başındaki ve sonundaki boşluğu at, boş satırları çıkar.
- Satırları sırala ve `"\n"` ile birleştir.

Özet: `hashlib.sha256(metin.encode()).hexdigest()`.

**Beklenen çıktı:**

```
pip-Linux-509b0a14
pip-Linux-509b0a14
pip-Linux-9c118a73
```
