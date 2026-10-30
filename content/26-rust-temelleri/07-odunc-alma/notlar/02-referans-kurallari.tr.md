## & işaretinin yerleri

| Yazım | Anlamı |
|---|---|
| `&x` | x'i ödünç al (okuma) |
| `&mut x` | x'i ödünç al (yazma) |
| `x: &T` | Parametre okuyan referans |
| `x: &mut T` | Parametre yazan referans |
| `*r` | Referansın gösterdiği değer |
| `&&T` | Referansa referans; nadir |

## let mut r = &x ile let r = &mut x farkı

Kafa karıştırıcı bir ikili:

```rust
fn main() {
    let a = 1;
    let b = 2;
    let mut r = &a;
    println!("{r}");
    r = &b;
    println!("{r}");

    let mut c = 3;
    let w = &mut c;
    *w = 30;
    println!("{c}");
}
```

```text
1
2
30
```

| Yazım | Değişken başka yeri gösterebilir mi | Gösterdiği değer değişebilir mi |
|---|---|---|
| `let r = &x` | Hayır | Hayır |
| `let mut r = &x` | **Evet** | Hayır |
| `let r = &mut x` | Hayır | **Evet** |
| `let mut r = &mut x` | Evet | Evet |

## Otomatik dereference

Metot çağrılırken `.` işareti gereken kadar `*` ekler. Bu yüzden `text.len()` hem `String` hem `&String` için aynı yazılır. Karşılaştırmada böyle değildir:
`&i32` ile `i32` doğrudan `==` ile karşılaştırılamaz, `*r == 5` yazılır.

## Referans da bir değerdir

`&T` `Copy`'dir: Aynı şeyi gösteren ikinci bir okuyucu oluşturmak serbesttir. `&mut T` `Copy` değildir, çünkü aynı anda iki yazan olamaz.

## Referansın boyutu

Referans bir adrestir, yani çok küçüktür: Bu makinede 8 bayt. Metin ne kadar büyük olursa olsun ödünç vermek aynı ucuzluktadır.
