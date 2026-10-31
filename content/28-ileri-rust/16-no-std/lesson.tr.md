# no_std

Şimdiye kadar yazdığımız her program bir işletim sisteminin üstünde çalıştı: Dosya açtı, kol başlattı, ekrana yazdı. Çamaşır makinesinin işlemcisinde ya da işletim sisteminin kendisinde bunların hiçbiri yoktur. Rust orada da çalışır, çünkü standart kütüphanesi katmanlıdır.

## Üç katman

| Katman | Gerektirdiği | İçindekiler |
|---|---|---|
| `core` | Hiçbir şey | `Option`, `Result`, dilimler, `Iterator`, `fmt`, atomikler |
| `alloc` | Bellek ayırıcı | `Vec`, `String`, `Box`, `Arc`, `BTreeMap` |
| `std` | İşletim sistemi | Dosya, kol, ağ, ortam değişkeni, `HashMap`, `println!` |

Üstteki alttakini kullanır. `std::option::Option` aslında `core::option::Option`'ın yeniden dışa açılmış hâlidir, yani bugüne kadar farkında olmadan `core` kullandın.

## İlk no_std kütüphane

`#![no_std]` crate'i `std` yerine `core`'a bağlar. Bu bölümde kolay deneyebilmek için `no_std` bir kütüphane yazıp sıradan bir programdan çağıracağız. Kök `Cargo.toml`:

```toml
[package]
name = "app"
version = "0.1.0"
edition = "2024"

[dependencies]
tiny = { path = "tiny" }
```

`tiny/src/lib.rs`:

```rust
#![no_std]

pub fn clamp_percent(value: i32) -> u8 {
    if value < 0 {
        0
    } else if value > 100 {
        100
    } else {
        value as u8
    }
}

pub fn first_word(text: &str) -> &str {
    text.split(' ').next().unwrap_or("")
}
```

`src/main.rs`:

```rust
use tiny::{clamp_percent, first_word};

fn main() {
    println!("{}", clamp_percent(150));
    println!("{}", first_word("hello there"));
}
```

```text
100
hello
```

Yerleşik türler, dilimler, `Option` ve `split` hep `core`'da, yani eksik bir şey hissetmedik. Sıradan program bu kütüphaneyi sorunsuz kullanıyor, çünkü `std` onun üstündedir.

## Ne kaybolur?

Derleyici sınırı kendisi denetler. `std`'ye dokunmak:

```rust
#![no_std]

use std::collections::HashMap;

pub fn empty() -> HashMap<u8, u8> {
    HashMap::new()
}
```

```text
error[E0433]: cannot find module or crate `std` in this scope
 --> tiny/src/lib.rs:3:5
  |
3 | use std::collections::HashMap;
  |     ^^^ use of unresolved module or unlinked crate `std`
  |
  = help: if you wanted to use a crate named `std`, use `cargo add std` to add it to
    your `Cargo.toml`

For more information about this error, try `rustc --explain E0433`.
```

Derleyicinin `cargo add std` önerisi burada yanıltıcıdır: `std` eklenecek bir crate değildir. Çözüm satırı silmek ya da `#![no_std]`'yi kaldırmaktır.

`Vec` artık hazır gelmez:

```rust
#![no_std]

pub fn numbers() -> Vec<u32> {
    Vec::new()
}
```

```text
error[E0425]: cannot find type `Vec` in this scope
 --> tiny/src/lib.rs:3:21
  |
3 | pub fn numbers() -> Vec<u32> {
  |                     ^^^ not found in this scope

error[E0433]: cannot find type `Vec` in this scope
 --> tiny/src/lib.rs:4:5
  |
4 |     Vec::new()
  |     ^^^ use of undeclared type `Vec`

Some errors have detailed explanations: E0425, E0433.
For more information about an error, try `rustc --explain E0425`.
```

Ekrana yazmak da yok, çünkü "ekran" işletim sisteminin kavramıdır:

```rust
#![no_std]

pub fn say() {
    println!("hello");
}
```

```text
error: cannot find macro `println` in this scope
 --> tiny/src/lib.rs:4:5
  |
4 |     println!("hello");
  |     ^^^^^^^
```

## alloc: Ayırıcı varsa

Ayırıcı varsa `Vec` ve `String` geri gelir. `alloc` crate'i derleyiciyle gelir ama elle açılır:

```rust
#![no_std]

extern crate alloc;

use alloc::string::{String, ToString};
use alloc::vec::Vec;

pub fn words(text: &str) -> Vec<String> {
    text.split(' ').map(|word| word.to_string()).collect()
}
```

```text
["one", "two"]
```

`HashMap` burada da yoktur, çünkü varsayılan hasher'ı rastgelelik için işletim sistemine gider. Sıralı harita `alloc::collections::BTreeMap` kullanılabilir.

## Ayırmadan yaşamak

Küçük cihazlarda ayırıcı hiç olmayabilir, olsa da "bellek bitti" durumu kabul edilemeyebilir. Çözüm: Kapasiteyi derlemede belirlemek. Üretici kod yazarken ayırma yerine const generic kullanılır:

```rust
#![no_std]

pub struct Stack<const N: usize> {
    items: [i32; N],
    len: usize,
}

impl<const N: usize> Stack<N> {
    pub const fn new() -> Self {
        Stack { items: [0; N], len: 0 }
    }

    pub fn push(&mut self, value: i32) -> Result<(), i32> {
        if self.len == N {
            return Err(value);
        }
        self.items[self.len] = value;
        self.len += 1;
        Ok(())
    }

    pub fn as_slice(&self) -> &[i32] {
        &self.items[..self.len]
    }
}
```

```rust
use tiny::Stack;

static EMPTY: Stack<2> = Stack::new();

fn main() {
    let mut stack = Stack::<2>::new();
    println!("{:?}", stack.push(1));
    println!("{:?}", stack.push(2));
    println!("{:?}", stack.push(3));
    println!("{:?} {:?}", stack.as_slice(), EMPTY.as_slice());
    println!("{}", size_of::<Stack<2>>());
}
```

```text
Ok(())
Ok(())
Err(3)
[1, 2] []
16
```

- Kapasite türün parçasıdır, boyut önceden bellidir: 2 tane `i32` ve bir `usize`, 16 bayt.
- Dolunca panik yok, ayırma yok: `Err(değer)` ile değer geri verilir.
- `const fn` sayesinde `static` içinde kurulabilir, program başlamadan hazırdır.

Metin üretmek için de `String` gerekmez. `core::fmt::Write` uygulanan her şeye `write!` yazabilir:

```rust
#![no_std]

use core::fmt::{self, Write};

pub struct Buffer<'a> {
    bytes: &'a mut [u8],
    len: usize,
}

impl<'a> Buffer<'a> {
    pub fn new(bytes: &'a mut [u8]) -> Self {
        Buffer { bytes, len: 0 }
    }

    pub fn as_bytes(&self) -> &[u8] {
        &self.bytes[..self.len]
    }
}

impl Write for Buffer<'_> {
    fn write_str(&mut self, text: &str) -> fmt::Result {
        let end = self.len + text.len();
        if end > self.bytes.len() {
            return Err(fmt::Error);
        }
        self.bytes[self.len..end].copy_from_slice(text.as_bytes());
        self.len = end;
        Ok(())
    }
}

pub fn format_reading(out: &mut Buffer, celsius: i32) -> fmt::Result {
    write!(out, "temp={celsius}C")
}
```

```rust
use tiny::{Buffer, format_reading};

fn main() {
    let mut storage = [0u8; 16];
    let mut buffer = Buffer::new(&mut storage);
    println!("{:?}", format_reading(&mut buffer, 21));
    println!("{}", str::from_utf8(buffer.as_bytes()).unwrap());

    let mut small = [0u8; 3];
    let mut buffer = Buffer::new(&mut small);
    println!("{:?}", format_reading(&mut buffer, 21));
}
```

```text
Ok(())
temp=21C
Err(Error)
```

Sığmayan metin hata döndürdü, program ayakta. Bu kalıp gömülü kodda sürekli geçer.

## Bellek ayırıcıyı görmek

`no_std` programda ayırıcıyı sen seçersin; `#[global_allocator]` bunun yoludur ve `std`'li programda da çalışır. Bütün ayırmaları sayalım:

```rust
use std::alloc::{GlobalAlloc, Layout, System};
use std::sync::atomic::{AtomicUsize, Ordering};

struct Counting;

static COUNT: AtomicUsize = AtomicUsize::new(0);

// SAFETY: every call is passed on to the system allocator unchanged.
unsafe impl GlobalAlloc for Counting {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        COUNT.fetch_add(1, Ordering::Relaxed);
        unsafe { System.alloc(layout) }
    }

    unsafe fn dealloc(&self, pointer: *mut u8, layout: Layout) {
        unsafe { System.dealloc(pointer, layout) }
    }
}

#[global_allocator]
static ALLOCATOR: Counting = Counting;

fn count_of(work: impl FnOnce()) -> usize {
    let before = COUNT.load(Ordering::Relaxed);
    work();
    COUNT.load(Ordering::Relaxed) - before
}

fn main() {
    println!("array: {}", count_of(|| {
        let values = [1u8; 64];
        std::hint::black_box(values);
    }));
    println!("one box: {}", count_of(|| {
        std::hint::black_box(Box::new(1u8));
    }));
    println!("grown: {}", count_of(|| {
        let mut values = Vec::with_capacity(4);
        values.extend_from_slice(&[1u8, 2, 3, 4]);
        std::hint::black_box(values);
    }));
}
```

```text
array: 0
one box: 1
grown: 1
```

Dizi yığında (stack) durduğu için hiç ayırma yapmadı. Aynı `GlobalAlloc`'u küçük bir cihazda sabit bir bellek bölgesinden verecek şekilde yazarsın. `unsafe impl`'dir, çünkü boyut ve hizalama sözünü tutmayan bir ayırıcı bütün programı bozar.

## Özet

- `core`: Hiçbir şey istemez. `alloc`: Ayırıcı ister. `std`: İşletim sistemi ister.
- `#![no_std]` sınırı derleyiciye denetletir.
- `extern crate alloc;` ile `Vec` ve `String` geri gelir.
- Ayırmadan: Const generic ile sabit kapasite, `core::fmt::Write` ile sabit tampon.
- `#[global_allocator]` bütün ayırmaları yöneten türü seçer.
