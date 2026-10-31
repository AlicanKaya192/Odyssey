## unsafe

| Yazım | Anlamı |
|---|---|
| `unsafe { ... }` | Söz bloğu |
| `unsafe fn` | Çağıran söz verir |
| `unsafe trait`, `unsafe impl` | Uygulayan söz verir |
| `*const T`, `*mut T` | Ham işaretçi |
| `ptr.add(n)` | `n` eleman ileri |
| `ptr::read`, `ptr::write` | Düşürmeden oku, yaz |
| `slice::from_raw_parts_mut` | İşaretçiden dilim |
| `// SAFETY:` | Neden güvenli |

## Bellek

| Yazım | Anlamı |
|---|---|
| `size_of::<T>()`, `align_of::<T>()` | Boyut, hizalama |
| `Layout::new::<T>()`, `Layout::array::<T>(n)` | Ayırma düzeni |
| `alloc`, `realloc`, `dealloc` | Elle bellek |
| `MaybeUninit::uninit()`, `assume_init` | Kurulmamış bellek |
| `ManuallyDrop` | Düşürmeyi durdurmak |
| `ptr::drop_in_place` | Yerinde düşürmek |
| `repr(C)`, `repr(transparent)` | Düzen sözü |
| `PhantomData<T>` | Sahiplik bilgisi |

## Kollar

| Yazım | Anlamı |
|---|---|
| `T: Send` | Sahiplik kola geçer |
| `T: Sync` | `&T` kola geçer |
| `unsafe impl Send for T {}` | Söz senin |
| `AtomicU32::fetch_add` | Atomik artırma |
| `compare_exchange(_weak)` | Bekleneni değiştir |
| `Relaxed` | Yalnız atomiklik |
| `Acquire`, `Release` | Yazılanı göster |
| `UnsafeCell<T>` | İç değişebilirliğin temeli |

## Async

| Yazım | Anlamı |
|---|---|
| `impl Future`, `poll` | Elle future |
| `Poll::Ready(v)`, `Poll::Pending` | Sonuç, henüz değil |
| `cx.waker().clone()` | Saklanacak waker |
| `wake()`, `wake_by_ref()` | Yeniden yokla |
| `impl Wake for T` | `Arc<T>`'den waker |
| `async fn`, `.await` | Durum makinesi |
| `pin!`, `Box::pin` | Sabitleme |
| `get_unchecked_mut`, `Pin::new_unchecked` | Alan sabitleme |

## Makro

| Yazım | Anlamı |
|---|---|
| `macro_rules! ad { (kalıp) => { şablon }; }` | Bildirimsel |
| `$x:expr`, `$t:ty`, `$n:ident`, `$a:tt` | Parçalar |
| `$( ... ),* $(,)?` | Tekrar, sondaki virgül |
| `#[proc_macro]`, `#[proc_macro_derive(N)]` | Procedural |
| `#[proc_macro_attribute]` | Öğeyi değiştiren |

## FFI

| Yazım | Anlamı |
|---|---|
| `unsafe extern "C" { fn f(); }` | C'den fonksiyon |
| `safe fn f();` | Güvenli bildirim |
| `#[unsafe(no_mangle)] pub extern "C" fn` | C'ye açık |
| `CString`, `CStr`, `c"text"` | C metni |
| `Box::into_raw`, `Box::from_raw` | Opak tutamaç |

## Katmanlar

| Yazım | Anlamı |
|---|---|
| `#![no_std]` | `core`'a bağlan |
| `extern crate alloc;` | `Vec`, `String`, `Box` |
| `#[panic_handler]` | Panikte ne olacak |
| `#[global_allocator]` | Ayırıcıyı seç |
