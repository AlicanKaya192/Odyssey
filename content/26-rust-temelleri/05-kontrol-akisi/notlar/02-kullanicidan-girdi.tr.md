Program dışarıdan veri alabilir. En basit yol **standart girdiden** bir satır okumaktır.

```rust
fn main() {
    let mut line = String::new();
    std::io::stdin().read_line(&mut line).expect("read failed");
    let name = line.trim();
    println!("Hello, {name}!");
}
```

Girdi olarak `Ada` verilirse:

```text
Hello, Ada!
```

Satır satır:

| Kod | Anlamı |
|---|---|
| `String::new()` | Büyüyebilen boş bir metin açar |
| `std::io::stdin()` | Standart girdi: klavye ya da yönlendirilen veri |
| `.read_line(&mut line)` | Bir satırı `line` metnine ekler |
| `.expect("...")` | Okuma başarısız olursa bu mesajla durur |
| `.trim()` | Baştaki ve sondaki boşlukları, satır sonunu atar |

`&mut line` "line'ı değiştirmen için ödünç veriyorum" demektir. Bunu yedinci bölümde göreceğiz. Şimdilik kalıp olarak yaz.

## Metni sayıya çevirmek

```rust
fn main() {
    let mut line = String::new();
    std::io::stdin().read_line(&mut line).expect("read failed");
    let n: i32 = line.trim().parse().expect("not a number");
    println!("{}", n * 2);
}
```

Girdi olarak `21` verilirse:

```text
42
```

`.parse()` metni sayıya çevirmeyi dener. Hangi türe çevireceğini `: i32` söylüyor. Başarısız olabilir (metin `abc` olabilir), onun için `.expect`
gerekiyor. Hataları nazikçe ele almayı on üçüncü bölümde öğreneceğiz.

## Bu patikada

Girdi isteyen alıştırmalarda Odyssey programına önceden hazırlanmış girdiyi verir. Programın kullanıcı gibi yazmanı beklemez.
