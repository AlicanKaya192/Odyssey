`checksum(path)` dosyanın **içeriğinin** SHA-256 özetini (onaltılık, tam)
döndürmeli. Dosyayı ikili kipte (`"rb"`) aç, 4096 baytlık parçalarla oku ve
her parçayı `update` ile ver (ya da `hashlib.file_digest`). Başlangıç kodu
dosyanın değil **adının** özetini alıyor.

**Beklenen çıktı:**

```
a6a364ba6b5c813b
e3b0c44298fc1c14
```
