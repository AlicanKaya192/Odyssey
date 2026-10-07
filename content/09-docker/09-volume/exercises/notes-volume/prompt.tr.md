`notes.py` kendisine verilen metni `/data/notes.txt`'ye ekleyip toplam not
sayısını yazıyor.

**Yapman gerekenler:**

1. Verinin `/data`'da durduğunu `VOLUME` ile belgele.
2. `ENTRYPOINT` ile her zaman `python notes.py` çalışsın (not argüman olarak
   gelecek).

Odyssey iki **ayrı** konteyner çalıştıracak, ikisine de aynı volume'u
bağlayarak (`-v notes:/data`): biri `buy milk`, öteki `call Ada` notunu
ekleyecek.

**Beklenen çıktılar:**

```
notes: 1
notes: 2
```
