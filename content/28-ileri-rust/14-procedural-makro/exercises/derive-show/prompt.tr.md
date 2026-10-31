`#[derive(Show)]` yaz: `fn show(&self) -> String` üretsin, sonuç `Point { x: 1, y: 2 }` biçiminde olsun (değerler `{:?}` ile). Alan adını tek `:`'den önceki ad olarak bul; `::`'ye aldanma.

**Beklenen çıktı:**

```text
Point { x: 1, y: 2 }
User { name: "ada", age: 36, tags: [1, 2] }
```
