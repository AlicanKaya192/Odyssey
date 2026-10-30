## Yazımlar

| Yer | Yazım |
|---|---|
| Fonksiyon | `fn f<'a>(x: &'a str) -> &'a str` |
| Değiştirilebilir | `&'a mut T` |
| Struct | `struct S<'a> { x: &'a str }` |
| impl | `impl<'a> S<'a> { ... }` |
| Generic ile | `fn f<'a, T>(x: &'a T) -> &'a T` |
| Çıkarılmış | `impl S<'_> { ... }` |
| Sabit | `&'static str` |

## Çıkarım örnekleri

| Yazdığın | Derleyicinin gördüğü |
|---|---|
| `fn f(x: &str) -> &str` | `fn f<'a>(x: &'a str) -> &'a str` |
| `fn f(x: &str, n: i32) -> &str` | Tek referans süresi: Aynı |
| `fn f(&self, y: &str) -> &str` | Dönen `self`'e bağlı |
| `fn f(x: &str, y: &str) -> &str` | **Belirsiz: E0106** |

## Hangi hata ne der?

| Kod | Anlamı | Genelde çözüm |
|---|---|---|
| `E0106` | İşaret eksik | `'a` ekle ya da sahipli döndür |
| `E0597` | Değer yeterince yaşamıyor | Kapsamı genişlet |
| `E0515` | Yerele referans dönüyor | Sahipli döndür |
| `E0499`, `E0502` | Ödünç çakışması | Kapsamı daralt |

## Süre sonu: Son kullanım

Referansın süresi kapsam sonuna değil, **son kullanımına** kadardır. Bu yüzden aşağıdaki derlenir:

```rust
fn main() {
    let mut list = vec![1, 2];
    let first = &list[0];
    println!("{first}");
    list.push(3);
    println!("{:?}", list);
}
```

```text
1
[1, 2, 3]
```

`first` son kez kullanıldıktan sonra `push` serbesttir.
