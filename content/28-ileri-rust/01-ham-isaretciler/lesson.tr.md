# Ham İşaretçiler

Referans dört söz verir: Geçerlidir, hizalıdır, gösterdiği yaşıyordur, `&mut` ise tektir. Ham işaretçi hiçbirini vermez. Bu özgürlüğün bedeli, sözleri senin tutmandır.

## Üretmek

```rust
fn main() {
    let mut value = 5;

    let a = &raw const value;
    let b = &raw mut value;

    // SAFETY: both pointers show value, which is alive; no reference is in use.
    unsafe {
        *b += 1;
        println!("{}", *a);
    }
}
```

```text
6
```

`&raw const x` ve `&raw mut x`, ara referans üretmeden işaretçi verir. Bu önemlidir, çünkü `&mut x as *mut _` önce bir `&mut` üretir ve o `&mut`'ın kuralları o anda geçerlidir.

Boş işaretçi de üretilebilir, ama okunamaz. `is_null` denetler; `as_ref` boşsa `None` verir:

```rust
use std::ptr;

fn main() {
    let value = 7;
    let good: *const i32 = &value;
    let bad: *const i32 = ptr::null();

    println!("{} {}", good.is_null(), bad.is_null());

    // SAFETY: as_ref checks null; good shows a live value.
    unsafe {
        println!("{:?}", good.as_ref());
        println!("{:?}", bad.as_ref());
    }
}
```

```text
false true
Some(7)
None
```

## Aritmetik

`p.add(i)` işaretçiyi `i` **öğe** ilerletir, `i` bayt değil. Türün boyutunu derleyici biliyor:

```rust
fn sum(list: &[i32]) -> i32 {
    let p = list.as_ptr();
    let mut total = 0;
    for i in 0..list.len() {
        // SAFETY: i < len, so p.add(i) is inside the slice.
        total += unsafe { *p.add(i) };
    }
    total
}

fn main() {
    println!("{}", sum(&[1, 2, 3]));
    println!("{}", size_of::<i32>());
}
```

```text
6
4
```

Dizinin sonundan bir sonrası üretilebilir ama okunamaz. Döngü `i < len` şartıyla bu yüzden güvende.

## Okumak ve yazmak

`*p` yazınca eski değer düşürülür. `ptr::write` ise eskisine dokunmaz:

```rust
use std::ptr;

struct Noisy(&'static str);

impl Drop for Noisy {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

fn main() {
    let mut a = Noisy("a");
    a = Noisy("b");
    println!("after assignment");

    let mut c = Noisy("c");
    // SAFETY: c is alive and valid; its old value only leaks.
    unsafe { ptr::write(&mut c, Noisy("d")) };
    println!("after write");
}
```

```text
drop a
after assignment
after write
drop d
drop b
```

| Çağrı | Ne yapar | Tuzağı |
|---|---|---|
| `*p = v` | Eskiyi düşürür, yeniyi yazar | Eski değer geçerli olmalı |
| `ptr::write(p, v)` | Eskiye bakmadan yazar | Eski değer sızar |
| `ptr::read(p)` | Bit bit kopyalar | İki sahip olur |

`ptr::read` özellikle tehlikelidir: Bir `String`'i okuyunca aynı belleğin iki sahibi olur, ikisi de silinmeye kalkarsa tanımsız davranış olur. Doğru kullanımı, kaynağı hemen üzerine yazmaktır. `mem::replace`'in yaptığı tam olarak budur:

```rust
use std::ptr;

fn take_and_set(slot: &mut String, new: String) -> String {
    // SAFETY: the read value is returned, and the slot is overwritten
    // at once, so there are never two owners at the end.
    unsafe {
        let old = ptr::read(slot);
        ptr::write(slot, new);
        old
    }
}

fn main() {
    let mut name = String::from("old");
    let previous = take_and_set(&mut name, String::from("new"));
    println!("{previous} {name}");
}
```

```text
old new
```

## Box ve ham işaretçi

`Box::into_raw` sahipliği bırakıp işaretçi verir. `Box::from_raw` sahipliği geri alır. Bağlı liste gibi yapılar böyle kurulur:

```rust
fn main() {
    let boxed = Box::new(String::from("hi"));
    let p: *mut String = Box::into_raw(boxed);

    // SAFETY: p came from Box::into_raw and nothing else uses it.
    unsafe {
        (*p).push_str(" there");
        let back = Box::from_raw(p);
        println!("{back}");
    }
}
```

```text
hi there
```

| Hata | Sonuç |
|---|---|
| `from_raw` hiç çağrılmaz | Bellek sızar |
| `from_raw` iki kez çağrılır | İki kez silinir, tanımsız davranış |
| `Box`'tan gelmeyen işaretçi | Tanımsız davranış |

## NonNull

`NonNull<T>`, boş olmadığına söz veren `*mut T`'dir. Asıl avantajı boyuttur: `Option<NonNull<T>>` işaretçiyle aynı boyuttadır, çünkü `None` için boş değeri kullanır.

```rust
use std::ptr::NonNull;

fn main() {
    println!("{}", size_of::<*const u32>());
    println!("{}", size_of::<NonNull<u32>>());
    println!("{}", size_of::<Option<NonNull<u32>>>());
    println!("{}", size_of::<Option<&u32>>());
    println!("{}", size_of::<Option<u32>>());
}
```

```text
8
8
8
8
8
```

Son satıra bak: `Option<u32>` 8 bayt tutarken, `Option<&u32>` ve `Option<NonNull<u32>>` işaretçinin kendisi kadar. Bu **boşluk iyileştirmesi** Rust'ın söz verdiği bir şeydir, tesadüf değil.

## Hiza

`u32` dört baytın katı olan adreslerde durur. `*p` ile hizasız okumak tanımsız davranıştır; bayt dizisinden sayı okurken `read_unaligned` gerekir:

```rust
fn main() {
    println!("{}", align_of::<u8>());
    println!("{}", align_of::<u32>());

    let bytes: [u8; 5] = [9, 1, 0, 0, 0];
    let p = bytes[1..].as_ptr() as *const u32;

    // SAFETY: four bytes are readable from p; read_unaligned allows any address.
    let number = unsafe { p.read_unaligned() };
    println!("{}", u32::from_le(number));
}
```

```text
1
4
1
```

## Özet

- `&raw const` ve `&raw mut` ara referans üretmez.
- `p.add(i)` öğe sayar; sınırların dışını okumak tanımsızdır.
- `*p =` eskiyi düşürür, `ptr::write` düşürmez, `ptr::read` iki sahip üretir.
- `Box::into_raw` ve `from_raw` tam bir kez eşleşir.
- `NonNull` boş olmaz, `Option<NonNull<T>>` ek yer tutmaz.
