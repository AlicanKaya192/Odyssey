# Kendi Vec'imiz

Şimdiye kadar öğrendiğimiz her şeyi tek türde birleştiriyoruz. `Vec<T>` sihir değildir: Üç alan, biraz `unsafe` ve dikkatli bir sıra. Sonunda `MyVec` standart olanın en önemli davranışlarını yapacak.

## Üç alan

<figure class="fig"><svg viewBox="0 0 640 284" width="640" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="20" y="24" font-size="13" font-weight="600">yığın (stack)</text><text class="dim" x="390" y="24" font-size="13" font-weight="600">öbek (heap)</text><g><rect class="box" x="20" y="44" width="230" height="44" rx="8"/><text class="ink" x="34" y="71" font-size="14" font-weight="600">ptr</text><text class="dim" x="110" y="71" font-size="12.5"></text></g><g><rect class="box" x="20" y="102" width="230" height="44" rx="8"/><text class="ink" x="34" y="129" font-size="14" font-weight="600">cap</text><text class="dim" x="110" y="129" font-size="12.5">4</text></g><g><rect class="box" x="20" y="160" width="230" height="44" rx="8"/><text class="ink" x="34" y="187" font-size="14" font-weight="600">len</text><text class="dim" x="110" y="187" font-size="12.5">2</text></g><g><rect class="box" x="390" y="44" width="220" height="44" rx="8"/><text class="ink" x="404" y="71" font-size="14">10</text></g><g><rect class="box" x="390" y="102" width="220" height="44" rx="8"/><text class="ink" x="404" y="129" font-size="14">20</text></g><g><rect class="box" x="390" y="160" width="220" height="44" rx="8"/><text class="ink" x="404" y="187" font-size="14">?</text></g><g><rect class="box" x="390" y="218" width="220" height="44" rx="8"/><text class="ink" x="404" y="245" font-size="14">?</text></g><path class="curve" d="M250 66 C320 66 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/></svg><figcaption>İlk iki yer dolu, son ikisi başlatılmamış: len 2, cap 4.</figcaption></figure>

| Alan | Anlamı |
|---|---|
| `ptr` | Öbekteki ilk öğeye işaretçi |
| `cap` | Kaç öğelik yer ayrıldı |
| `len` | Kaç öğe gerçekten dolu |

Asıl kural, **değişmez** (invariant) denen şu cümle: `0..len` arasındaki yerler dolu ve geçerli, `len..cap` arasındakiler başlatılmamış. Her `unsafe` satır bu cümleye güvenir.

## Bellek ayırmak

`Box` ve `Vec` kullanmadan bellek almak için `std::alloc` var. Ne kadar yer istediğini `Layout` söyler:

```rust
use std::alloc::{self, Layout};
use std::ptr::{self, NonNull};

struct MyVec<T> {
    ptr: NonNull<T>,
    cap: usize,
    len: usize,
}

impl<T> MyVec<T> {
    fn new() -> Self {
        assert!(size_of::<T>() != 0, "zero-sized types are not handled");
        MyVec { ptr: NonNull::dangling(), cap: 0, len: 0 }
    }

    fn grow(&mut self) {
        let new_cap = if self.cap == 0 { 4 } else { self.cap * 2 };
        let new_layout = Layout::array::<T>(new_cap).unwrap();

        let new_ptr = if self.cap == 0 {
            // SAFETY: T is not zero-sized, so the layout size is not zero.
            unsafe { alloc::alloc(new_layout) }
        } else {
            let old_layout = Layout::array::<T>(self.cap).unwrap();
            let old_ptr = self.ptr.as_ptr().cast::<u8>();
            // SAFETY: old_ptr came from alloc with old_layout.
            unsafe { alloc::realloc(old_ptr, old_layout, new_layout.size()) }
        };

        self.ptr = match NonNull::new(new_ptr.cast::<T>()) {
            Some(p) => p,
            None => alloc::handle_alloc_error(new_layout),
        };
        self.cap = new_cap;
    }
}

```

Dört şeye bak:

1. `NonNull::dangling()`: Boş `Vec` hiç bellek ayırmaz, ama `ptr` boş olamaz. Hizalı ama geçersiz bir adres koyuyoruz. `len` 0 olduğu için hiç okunmaz.
2. Kapasite ikiye katlanıyor. Her `push`'ta yeniden ayırmak çok yavaş olurdu.
3. `realloc` eski yeri büyütür ya da başka yere taşır. Bu yüzden eski `ptr` artık geçersizdir.
4. Boyut sıfır bellek ayırmak tanımsız davranıştır. `()` gibi türleri bu sürümde `assert!` ile reddediyoruz.

## push ve pop

```rust
impl<T> MyVec<T> {
    fn push(&mut self, value: T) {
        if self.len == self.cap {
            self.grow();
        }
        // SAFETY: len < cap, so the place is inside the allocation and empty.
        unsafe { ptr::write(self.ptr.as_ptr().add(self.len), value) };
        self.len += 1;
    }

    fn pop(&mut self) -> Option<T> {
        if self.len == 0 {
            return None;
        }
        self.len -= 1;
        // SAFETY: the place was filled, and len no longer covers it.
        Some(unsafe { ptr::read(self.ptr.as_ptr().add(self.len)) })
    }
}

```

Sıra önemli: `push`'ta önce yazılır, **sonra** `len` artar. `pop`'ta önce `len` azalır, **sonra** okunur. Böylece her an değişmez doğrudur.

`ptr::write` kullanıyoruz, çünkü `*p = value` eski değeri düşürmeye kalkardı, ve orada eski değer yok. `ptr::read` sahipliği çıkarıyor; `len` azaldığı için o yere bir daha bakılmayacak.

## Drop

Şu ana kadar bellek geri verilmiyor ve öğeler düşürülmüyor. İkisi de gerekli:

```rust
impl<T> Drop for MyVec<T> {
    fn drop(&mut self) {
        while self.pop().is_some() {}
        if self.cap != 0 {
            let layout = Layout::array::<T>(self.cap).unwrap();
            // SAFETY: ptr came from alloc or realloc with this layout.
            unsafe { alloc::dealloc(self.ptr.as_ptr().cast::<u8>(), layout) };
        }
    }
}

struct Noisy(&'static str);

impl Drop for Noisy {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

fn main() {
    let mut list = MyVec::new();
    list.push(Noisy("a"));
    for name in ["b", "c", "d", "e"] {
        list.push(Noisy(name));
    }
    println!("cap {} len {}", list.cap, list.len);
    let last = list.pop();
    println!("popped");
    drop(last);
    println!("dropping the list");
}
```

```text
cap 8 len 5
popped
drop e
dropping the list
drop d
drop c
drop b
drop a
```

Önce öğeler (`pop` döngüsü), sonra bellek. `cap == 0` ise hiç ayrılmadı, geri verilecek bir şey yok. Kapasite büyürken hiçbir öğenin düşmediğine dikkat et: `realloc` bitleri taşır, değer sayısı aynı kalır.

## Deref ile bütün dilim yöntemleri

Tek bir `Deref` yazınca `iter`, `len`, `sort`, `[i]` ve dilimin bütün yöntemleri bedava gelir. Bu, `Vec`'in de yaptığı şeydir:

```rust
use std::ops::{Deref, DerefMut};
use std::slice;

impl<T> Deref for MyVec<T> {
    type Target = [T];

    fn deref(&self) -> &[T] {
        // SAFETY: the first len places are filled, and ptr is aligned and not null.
        unsafe { slice::from_raw_parts(self.ptr.as_ptr(), self.len) }
    }
}

impl<T> DerefMut for MyVec<T> {
    fn deref_mut(&mut self) -> &mut [T] {
        // SAFETY: as above, and &mut self gives unique access.
        unsafe { slice::from_raw_parts_mut(self.ptr.as_ptr(), self.len) }
    }
}

fn main() {
    let mut list = MyVec::new();
    for n in [3, 1, 2] {
        list.push(n);
    }
    list.sort();
    list[0] = 10;
    println!("{} {:?}", list.len(), list.iter().max());
    println!("{:?}", &list[1..]);
}
```

```text
3 Some(10)
[2, 3]
```

## IntoIterator

Sahipliği alan iterator biraz incedir: `MyVec` düşürülmemeli, yoksa öğeleri iki kez siler. Bunun için `ManuallyDrop`:

```rust
use std::mem::ManuallyDrop;

struct IntoIter<T> {
    ptr: NonNull<T>,
    cap: usize,
    start: usize,
    end: usize,
}

impl<T> IntoIterator for MyVec<T> {
    type Item = T;
    type IntoIter = IntoIter<T>;

    fn into_iter(self) -> IntoIter<T> {
        let me = ManuallyDrop::new(self);
        IntoIter { ptr: me.ptr, cap: me.cap, start: 0, end: me.len }
    }
}

impl<T> Iterator for IntoIter<T> {
    type Item = T;

    fn next(&mut self) -> Option<T> {
        if self.start == self.end {
            return None;
        }
        // SAFETY: start..end are filled, and start moves past this place.
        let value = unsafe { ptr::read(self.ptr.as_ptr().add(self.start)) };
        self.start += 1;
        Some(value)
    }
}

impl<T> Drop for IntoIter<T> {
    fn drop(&mut self) {
        for _ in &mut *self {}
        if self.cap != 0 {
            let layout = Layout::array::<T>(self.cap).unwrap();
            // SAFETY: ptr came from MyVec with this layout, and MyVec did not drop.
            unsafe { alloc::dealloc(self.ptr.as_ptr().cast::<u8>(), layout) };
        }
    }
}

fn main() {
    let mut list = MyVec::new();
    for name in ["a", "b", "c"] {
        list.push(Noisy(name));
    }
    for item in list {
        if item.0 == "b" {
            break;
        }
    }
    println!("end");
}
```

```text
drop a
drop b
drop c
end
```

İterator yarıda bırakılırsa kalan öğeleri kendi `Drop`'u düşürür. Çıktıda `a` döngüde alınıp düşüyor, `b` döngüde kırılınca düşüyor, `c` ise iterator düşerken.

## Gerçek Vec'te neler var?

| Bu sürümde | Gerçeğinde |
|---|---|
| ZST reddi | `()` için hiç ayırmaz, sayar |
| Kapasite taşması `unwrap` | `isize::MAX` denetimi |
| Kod tek türde | `RawVec`'e bölünmüş, kod tekrarı az |
| `T` için `Send` yok | `unsafe impl Send` var (ileride) |

## Özet

- Değişmez: `0..len` dolu, `len..cap` boş. Her satır buna güvenir.
- `alloc`, `realloc`, `dealloc` ve `Layout::array`.
- `push`'ta önce yaz sonra `len`, `pop`'ta önce `len` sonra oku.
- `Drop`: Önce öğeler, sonra bellek.
- `Deref<Target = [T]>` bütün dilim yöntemlerini verir.
