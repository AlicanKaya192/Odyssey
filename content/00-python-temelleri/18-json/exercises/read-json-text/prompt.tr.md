`text` değişkeninde bir kitabın JSON metni duruyor.

**Yapman gerekenler:**

1. `json` modülünü içe aktar.
2. `json.loads` ile metni `book` adında bir sözlüğe çevir.
3. Sırayla yazdır: `book`'un türü (`type(book)`), kitabın adı ve yazarı
   (aralarında `by`), kitabın 2026'da kaç yaşında olduğu
   (`2026 - book["year"]`) ve `book["available"]`.

**Beklenen çıktı:**

```text
<class 'dict'>
Dune by Frank Herbert
61
True
```

`available` JSON'da `true` yazılmış; Python'da ne olarak geldiğine dikkat et.
