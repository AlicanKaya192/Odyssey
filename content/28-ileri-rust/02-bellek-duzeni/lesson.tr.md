# Bellek Düzeni: repr

Bir struct bellekte nasıl durur? Çoğu zaman bilmen gerekmez. Ama kendi `Vec`'ini yazarken, C ile konuşurken ya da belleği küçültürken gerekir.

## Boyut ve hiza

Her türün bir **boyutu** ve bir **hizası** var. Hiza, türün hangi adreslerde durabileceğini söyler: `align_of::<u32>()` 4 ise adres 4'ün katı olmalı. Boyut her zaman hizanın katıdır, çünkü dizide öğeler yan yana durur.

```rust
struct Empty;

fn main() {
    println!("u8 {} {}", size_of::<u8>(), align_of::<u8>());
    println!("u32 {} {}", size_of::<u32>(), align_of::<u32>());
    println!("u64 {} {}", size_of::<u64>(), align_of::<u64>());
    println!("() {}", size_of::<()>());
    println!("Empty {}", size_of::<Empty>());
    println!("[u32; 3] {}", size_of::<[u32; 3]>());
}
```

```text
u8 1 1
u32 4 4
u64 8 8
() 0
Empty 0
[u32; 3] 12
```

Sıfır boyutlu türler (`()` ve alansız struct) gerçekten yer tutmaz. `Vec<()>` hiç bellek ayırmaz.

## Alan sırası

Alanlar arasına hiza için boşluk girer. Üç alanlı aynı struct, sıraya göre farklı boyuttadır. Varsayılan Rust düzeni boşluğu azaltmak için alanları **yeniden sıralayabilir**; `#[repr(C)]` ise yazdığın sırayı ve C'nin kurallarını kullanır:

```rust
use std::mem::offset_of;

#[repr(C)]
struct WithC {
    a: u8,
    b: u32,
    c: u8,
}

struct WithRust {
    a: u8,
    b: u32,
    c: u8,
}

#[repr(C)]
struct Sorted {
    b: u32,
    a: u8,
    c: u8,
}

fn main() {
    println!("{}", size_of::<WithC>());
    println!("{}", size_of::<WithRust>());
    println!("{}", size_of::<Sorted>());
    println!("{} {} {}", offset_of!(WithC, a), offset_of!(WithC, b), offset_of!(WithC, c));
}
```

```text
12
8
8
0 4 8
```

Bayt bayt:

```text
repr(C)   a . . . b b b b c . . .
Rust      b b b b a c . .
Sorted    b b b b a c . .
```

`.` boşluktur. `repr(C)` 12 bayt tutuyor, Rust düzeni 8. Varsayılan düzende alan sırası **söz değildir**: Sürüm değişince değişebilir, bu yüzden dosyaya yazma ya da C'ye geçme için `repr(C)` şart.

`repr(C)`'de düzeni sen iyileştirirsin: En büyük hizalı alan öne.

## Sıkıştırmak

`#[repr(packed)]` bütün boşlukları kaldırır, ama alanlar hizasız kalır. Hizasız alana referans almak bu yüzden yasak:

```rust
#[repr(C, packed)]
struct Tight {
    a: u8,
    b: u32,
}

fn main() {
    let t = Tight { a: 1, b: 2 };
    let r = &t.b;
    println!("{r}");
}
```

```text
error[E0793]: reference to field of packed struct is unaligned
 --> main.rs:9:13
  |
9 |     let r = &t.b;
  |             ^^^^
  |
  = note: this struct is 1-byte aligned, but the type of this field may require higher
    alignment
  = note: creating a misaligned reference is undefined behavior (even if that reference
    is never dereferenced)
  = help: copy the field contents to a local variable, or replace the reference with a
    raw pointer and use `read_unaligned`/`write_unaligned` (loads and stores via `*p`
    must be properly aligned even when using raw pointers)
```

Değeri önce kopyalamak güvenlidir:

```rust
#[repr(C, packed)]
struct Tight {
    a: u8,
    b: u32,
}

fn main() {
    let t = Tight { a: 1, b: 2 };
    let b = t.b;
    println!("{} {b}", size_of::<Tight>());
    println!("{}", t.a);
}
```

```text
5 2
1
```

`#[repr(align(N))]` tersini yapar, hizayı büyütür. Kollar birbirinin önbellek satırını kirletmesin diye kullanılır (Atomikler bölümü).

## Enum düzeni

Enum, hangi kolda olduğunu saklayan bir **etiket** (tag) taşır. Ama kullanılmayan değerler varsa etiket gerekmez:

```rust
#[repr(u8)]
#[derive(Clone, Copy)]
enum Level {
    Low = 1,
    High = 9,
}

fn main() {
    println!("{}", size_of::<Option<bool>>());
    println!("{}", size_of::<Option<char>>());
    println!("{}", size_of::<Option<u8>>());
    println!("{}", size_of::<Option<Box<u8>>>());
    println!("{}", size_of::<Level>());
    println!("{} {}", Level::Low as u8, Level::High as u8);
}
```

```text
1
4
2
8
1
1 9
```

| Tür | Boyut | Neden |
|---|---|---|
| `Option<bool>` | 1 | `bool` yalnızca 0 ve 1, `None` 2 oluyor |
| `Option<char>` | 4 | `char`'ın geçersiz değerleri var |
| `Option<u8>` | 2 | `u8`'in boş değeri yok, etiket şart |
| `Option<Box<u8>>` | 8 | `Box` boş olamaz |

`#[repr(u8)]` etiketi sayıya bağlar, `as u8` ile okunur.

## repr(transparent)

Tek alanlı sarmalayıcının düzeni, alanın düzeniyle aynı olsun der. Böylece `&[Meters]`, `&[f64]`'e güvenle çevrilebilir:

```rust
use std::slice;

#[repr(transparent)]
struct Meters(f64);

fn as_numbers(list: &[Meters]) -> &[f64] {
    // SAFETY: Meters has the layout of f64, so the same bytes are valid.
    unsafe { slice::from_raw_parts(list.as_ptr().cast::<f64>(), list.len()) }
}

fn main() {
    let list = [Meters(1.5), Meters(2.5)];
    println!("{:?}", as_numbers(&list));
    println!("{}", size_of::<Meters>());
}
```

```text
[1.5, 2.5]
8
```

## Şişman işaretçiler

Bazı referanslar iki sözcüktür, çünkü işaretçinin yanında ek bilgi taşır:

```rust
fn main() {
    println!("{}", size_of::<&u8>());
    println!("{}", size_of::<&[u8]>());
    println!("{}", size_of::<&str>());
    println!("{}", size_of::<&dyn std::fmt::Debug>());
    println!("{}", size_of::<Box<[u8]>>());
    println!("{}", size_of::<String>());
    println!("{}", size_of::<Vec<u8>>());
}
```

```text
8
16
16
16
16
24
24
```

| Tür | İkinci sözcük |
|---|---|
| `&[T]`, `&str` | Uzunluk |
| `&dyn Trait` | Sanal tablo adresi |

## Özet

- Boyut, hizanın katıdır; alanlar arasına boşluk girer.
- Rust düzeni alanları yeniden sıralar, bu bir söz değildir.
- `repr(C)`: Yazılan sıra, C kuralları. Dosya ve FFI için.
- `repr(packed)`: Boşluk yok, alana referans yok.
- Enum, boş değer varsa etiketsiz durur: `Option<&T>`.
- `repr(transparent)`: Sarmalayıcı, alanıyla aynı düzende.
