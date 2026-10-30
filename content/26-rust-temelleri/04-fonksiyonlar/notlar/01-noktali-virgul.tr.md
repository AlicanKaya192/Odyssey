## Tek bir işaretin anlamı

Rust'ta noktalı virgül "bu değeri at" demektir. İki sürümü yan yana gör:

<figure class="fig"><div class="versus"><div><h4>Değer döner</h4><code>fn f() -&gt; i32 { 5 }</code><br>Blok 5 değerini verir.</div><div><h4>Hata</h4><code>fn f() -&gt; i32 { 5; }</code><br>Blok <code>()</code> verir, ama <code>i32</code> vaat edilmişti.</div></div><figcaption>Aradaki tek fark bir noktalı virgül.</figcaption></figure>

## Nerede gerekir, nerede gerekmez?

| Yer | Noktalı virgül |
|---|---|
| `let` satırının sonu | Gerekir |
| `println!(...)` satırının sonu | Gerekir, sonda ise değer `()` olduğu için fark etmez |
| Dönüş değeri olan son ifade | **Olmaz** |
| `fn` gövdesinin kapanış `}` sonrası | Gerekmez |
| `if`, `for` bloğunun kapanışı sonrası | Gerekmez |
| `return x` | Yazılır (`return x;`), son satırsa kalıp gereği de olur |

## Dönüş türünü unutursan

Bu da sık görülür:

```rust
fn double(n: i32) {
    n * 2
}

fn main() {
    double(2);
}
```

```text
error[E0308]: mismatched types
 --> main.rs:2:5
  |
1 | fn double(n: i32) {
  |                  - help: try adding a return type: `-> i32`
2 |     n * 2
  |     ^^^^^ expected `()`, found `i32`
```

Gövde `i32` veriyor ama imza hiçbir şey vaat etmiyor. Çözüm imzaya `-> i32` eklemek. `help:` satırı bunu söyler.

## Fonksiyon adı kuralları

| Öğe | Biçim | Örnek |
|---|---|---|
| Fonksiyon | `snake_case` | `total_price` |
| Değişken | `snake_case` | `user_name` |
| Sabit | `SCREAMING_SNAKE_CASE` | `MAX_SIZE` |
| Tür, trait | `PascalCase` | `UserAccount` |

Derleyici bu kurallara uymayan adlarda uyarır.
