Bu Dockerfile API anahtarını `ENV` ile imaja gömüyor: imajı alan herkes
`docker image inspect` ile görebilir.

**Yapman gereken:** anahtarı imajdan çıkar. `app.py` anahtarı zaten ortam
değişkeninden okuyor; anahtar çalıştırırken verilecek.

Odyssey imajda `API_KEY` olmadığını denetleyecek ve konteyneri
`-e API_KEY=test-key-123` ile çalıştıracak.

**Beklenen çıktı:**

```
key loaded: 12 chars
```
