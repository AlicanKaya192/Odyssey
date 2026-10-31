# FFI: C ile Konuşmak

İşletim sistemleri, veritabanları, grafik ve şifreleme kütüphanelerinin çoğu C arayüzü sunar. Rust'tan bunları çağırmaya, ya da Rust kodunu başka dillerden çağrılabilir yapmaya **FFI** (Foreign Function Interface, yabancı fonksiyon arayüzü) denir.

C, programlamanın ortak dilidir: Python'dan Java'ya çoğu dil birbiriyle C kurallarıyla konuşur. Bu yüzden C ile konuşmayı öğrenmek, hepsiyle konuşmayı öğrenmektir.

Bu bölüm için C derleyicisi gerekmiyor: Rust programları zaten C çalışma kitaplığına bağlanır, ondaki fonksiyonları doğrudan çağıracağız.

## İlk çağrı

Yabancı fonksiyonu tanıtmak için imzasını yazarız:

```rust
use std::ffi::c_int;

unsafe extern "C" {
    fn abs(n: c_int) -> c_int;
}

fn main() {
    let value = unsafe { abs(-7) };
    println!("{value}");
}
```

```text
7
```

- `extern "C"`: Bu fonksiyon C'nin çağrı kuralını (ABI, argümanların nasıl geçtiği) kullanır.
- `c_int`: C'nin `int`'i. Boyutu platforma göre değişebildiği için `i32` yazmak yerine bu ad kullanılır.
- `unsafe extern`: İmzayı biz yazdık, derleyici doğru mu bilemez. Yanlış yazarsak tanımsız davranış olur.

Çağrının kendisi de `unsafe` ister:

```rust
use std::ffi::c_int;

unsafe extern "C" {
    fn abs(n: c_int) -> c_int;
}

fn main() {
    println!("{}", abs(-7));
}
```

```text
error[E0133]: call to unsafe function `abs` is unsafe and requires unsafe block
 --> main.rs:8:20
  |
8 |     println!("{}", abs(-7));
  |                    ^^^^^^^ call to unsafe function
  |
  = note: consult the function's documentation for information on how to avoid undefined
    behavior
```

`abs` her girdi için güvenliyse bunu bildirimde söyleyebiliriz. `safe fn`, çağrıyı sıradan bir fonksiyona çevirir; söz artık bildirimi yazanındır:

```rust
use std::ffi::c_int;

unsafe extern "C" {
    safe fn abs(n: c_int) -> c_int;
}

fn main() {
    println!("{}", abs(-7));
}
```

```text
7
```

## Metinler: En sık sorun

Rust'ın `&str`'si bir işaretçi ve bir uzunluktur. C metni ise yalnızca işaretçidir; sonu **NUL baytıyla** (`0`) bellidir. İkisi aynı şey değildir:

```rust
use std::ffi::c_char;

unsafe extern "C" {
    fn strlen(text: *const c_char) -> usize;
}

fn main() {
    let length = unsafe { strlen("hello") };
    println!("{length}");
}
```

```text
error[E0308]: mismatched types
 --> main.rs:8:34
  |
8 |     let length = unsafe { strlen("hello") };
  |                           ------ ^^^^^^^ expected `*const i8`, found `&str`
  |                           |
  |                           arguments to this function are incorrect
  |
  = note: expected raw pointer `*const i8`
               found reference `&'static str`
note: function defined here
 --> main.rs:4:8
  |
4 |     fn strlen(text: *const c_char) -> usize;
  |        ^^^^^^ ----
```

Rust'tan C'ye metin göndermek için `CString`:

```rust
use std::ffi::{CString, c_char};

unsafe extern "C" {
    fn strlen(text: *const c_char) -> usize;
}

fn main() {
    let text = CString::new("hello").unwrap();
    let length = unsafe { strlen(text.as_ptr()) };
    println!("{length}");
    println!("{:?}", text.as_bytes_with_nul());
}
```

```text
5
[104, 101, 108, 108, 111, 0]
```

İkinci satır sondaki `0`'ı gösteriyor. C uzunluğu bayt sayarak bulur, yani harf değil bayt sayar:

```rust
use std::ffi::{CString, c_char};

unsafe extern "C" {
    fn strlen(text: *const c_char) -> usize;
}

fn main() {
    let text = CString::new("çay").unwrap();
    println!("{}", unsafe { strlen(text.as_ptr()) });
    println!("{}", "çay".chars().count());
}
```

```text
4
3
```

Metnin ortasında NUL olursa C metni orada bitirir. `CString::new` bu yüzden hata döndürür:

```rust
use std::ffi::CString;

fn main() {
    println!("{:?}", CString::new("a\0b"));
    println!("{:?}", CString::new("ab"));
}
```

```text
Err(NulError(1, [97, 0, 98]))
Ok("ab")
```

Metin sabitse `c"..."` yazımı `&CStr` verir, ayırma gerekmez:

```rust
use std::ffi::c_char;

unsafe extern "C" {
    fn strlen(text: *const c_char) -> usize;
}

fn main() {
    println!("{}", unsafe { strlen(c"hello".as_ptr()) });
}
```

```text
5
```

## Güvenli sarmalayıcı

FFI kodunun doğru biçimi şudur: `unsafe` küçük bir fonksiyonun içinde kalır, dışarıya güvenli bir arayüz çıkar.

```rust
use std::ffi::{CString, c_char};

unsafe extern "C" {
    fn strlen(text: *const c_char) -> usize;
}

fn c_length(text: &str) -> Option<usize> {
    let text = CString::new(text).ok()?;
    // SAFETY: text is a valid, NUL-terminated string for the whole call.
    Some(unsafe { strlen(text.as_ptr()) })
}

fn main() {
    println!("{:?}", c_length("hello"));
    println!("{:?}", c_length("a\0b"));
}
```

```text
Some(5)
None
```

Çağıran artık hiçbir söz vermiyor. NUL sorunu `None`'a dönüştü, `unsafe` tek satırda ve gerekçesi yanında.

## C'den gelen metin

Ters yönde `CStr` kullanılır: C'nin işaretçisini ödünç alır. C fonksiyonları "yok" demek için boş işaretçi döndürebilir, bu yüzden önce ona bakılır:

```rust
use std::ffi::{CStr, c_char};

unsafe extern "C" {
    fn getenv(name: *const c_char) -> *const c_char;
}

fn env_var(name: &CStr) -> Option<String> {
    // SAFETY: name is a valid, NUL-terminated string.
    let value = unsafe { getenv(name.as_ptr()) };
    if value.is_null() {
        return None;
    }
    // SAFETY: getenv gave a NUL-terminated string, and we copy it at once.
    Some(unsafe { CStr::from_ptr(value) }.to_string_lossy().into_owned())
}

fn main() {
    println!("{:?}", env_var(c"ODYSSEY_NOT_SET"));
    let text = c"from c";
    println!("{:?}", text.to_str());
}
```

```text
None
Ok("from c")
```

`CStr` ödünçtür, belleğin sahibi C'dir. Saklayacaksan hemen `String`'e kopyala.

## Geri çağrı

C'ye fonksiyon da verebiliriz. C'nin sıralama fonksiyonu `qsort`, karşılaştırmayı bizim fonksiyonumuzla yapar:

```rust
use std::ffi::{c_int, c_void};

unsafe extern "C" {
    fn qsort(
        base: *mut c_void,
        count: usize,
        size: usize,
        compare: extern "C" fn(*const c_void, *const c_void) -> c_int,
    );
}

extern "C" fn compare_i32(a: *const c_void, b: *const c_void) -> c_int {
    // SAFETY: qsort gives pointers into the i32 slice we passed.
    let (a, b) = unsafe { (*(a as *const i32), *(b as *const i32)) };
    a.cmp(&b) as c_int
}

fn main() {
    let mut values = [5, 1, 4, 2];
    // SAFETY: the pointer, count and size all describe the same array.
    unsafe {
        qsort(
            values.as_mut_ptr().cast(),
            values.len(),
            size_of::<i32>(),
            compare_i32,
        );
    }
    println!("{values:?}");
}
```

```text
[1, 2, 4, 5]
```

Geri çağrının kendisi de `extern "C"` olmalıdır. C türleri bilmez: `*const c_void` "bir şeyin adresi" demektir, doğru türe biz çeviririz. Kapanış verilemez, çünkü kapanışın yakaladıkları için C'de yer yoktur.

## Panik sınırı geçemez

`extern "C"` fonksiyondan panik dışarı çıkamaz, C yığın açmayı bilmez. Rust süreci hemen sonlandırır:

```rust
extern "C" fn boom() {
    panic!("inside the callback");
}

fn main() {
    boom();
    println!("never printed");
}
```

```text
thread 'main' panicked at main.rs:2:5:
inside the callback
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace

panic in a function that cannot unwind
thread caused non-unwinding panic. aborting.
```

(Çıktıdaki yığın dökümünü kısalttık.) C'nin çağıracağı fonksiyonda bu olmamalıysa `catch_unwind` ile yakalanıp hata koduna çevrilir:

```rust
use std::ffi::c_int;
use std::panic::catch_unwind;

extern "C" fn risky(n: c_int) -> c_int {
    match catch_unwind(|| 100 / n) {
        Ok(value) => value,
        Err(_) => -1,
    }
}

fn main() {
    println!("{}", risky(5));
    println!("{}", risky(0));
}
```

```text
20
-1
```

## Rust'ı dışarı açmak

Ters yön: Rust fonksiyonunu C'nin çağırması. İki şey gerekir: C'nin çağrı kuralı ve değişmeyen ad. Rust normalde adları değiştirir (mangling); `#[unsafe(no_mangle)]` bunu kapatır. Bu, bağlayıcının isimle bulmasını sağlar. `unsafe` yazımı, aynı adı iki kez kullanmanın bağlamayı bozabileceğini hatırlatır.

Burada C yok, ama aynı adı C'nin göreceği gibi ayrı bir bildirimle çağırabiliriz:

```rust
mod rust_side {
    #[unsafe(no_mangle)]
    pub extern "C" fn rust_add(a: i32, b: i32) -> i32 {
        a + b
    }
}

mod c_view {
    unsafe extern "C" {
        pub fn rust_add(a: i32, b: i32) -> i32;
    }
}

fn main() {
    let _keep = rust_side::rust_add;
    println!("{}", unsafe { c_view::rust_add(2, 3) });
}
```

```text
5
```

C, Rust türlerini bilmez. Rust nesnesini dışarı vermenin yolu **opak işaretçidir**: C yalnızca adresi tutar, içini görmez, her iş için bize geri verir.

```rust
pub struct Counter {
    total: u32,
}

#[unsafe(no_mangle)]
pub extern "C" fn counter_new() -> *mut Counter {
    Box::into_raw(Box::new(Counter { total: 0 }))
}

/// # Safety
/// `counter` must come from `counter_new` and must not be freed yet.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn counter_add(counter: *mut Counter, amount: u32) -> u32 {
    let counter = unsafe { &mut *counter };
    counter.total += amount;
    counter.total
}

/// # Safety
/// `counter` must come from `counter_new` and is invalid after this call.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn counter_free(counter: *mut Counter) {
    if !counter.is_null() {
        drop(unsafe { Box::from_raw(counter) });
    }
}

fn main() {
    let counter = counter_new();
    unsafe {
        counter_add(counter, 2);
        println!("{}", counter_add(counter, 3));
        counter_free(counter);
    }
}
```

```text
5
```

C tarafının göreceği başlık şuna benzer:

```text
typedef struct Counter Counter;

Counter *counter_new(void);
uint32_t counter_add(Counter *counter, uint32_t amount);
void counter_free(Counter *counter);
```

`Box::into_raw` sahipliği işaretçiye çevirir, `Box::from_raw` geri alır. Bir kütüphaneyi gerçekten dışarı açmak için `Cargo.toml`'a `crate-type = ["cdylib"]` yazılır.

## Özet

- `unsafe extern "C" { ... }` yabancı fonksiyonu tanıtır, imzanın doğruluğu bize aittir.
- Metin: `CString` Rust'tan C'ye, `CStr` C'den Rust'a, `c"..."` sabit.
- `unsafe`'i güvenli bir sarmalayıcının içinde tut.
- C dönen işaretçiye önce `is_null` ile bak.
- Panik `extern "C"` sınırını geçemez, süreç sonlanır; `catch_unwind` ile hata koduna çevir.
- Dışarı açmak: `#[unsafe(no_mangle)]`, `extern "C"`, opak işaretçi.
