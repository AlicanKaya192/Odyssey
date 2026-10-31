## unsafe

| Form | Meaning |
|---|---|
| `unsafe { ... }` | A promise block |
| `unsafe fn` | The caller promises |
| `unsafe trait`, `unsafe impl` | The implementer promises |
| `*const T`, `*mut T` | Raw pointers |
| `ptr.add(n)` | `n` elements forward |
| `ptr::read`, `ptr::write` | Read, write without dropping |
| `slice::from_raw_parts_mut` | A slice from a pointer |
| `// SAFETY:` | Why it is safe |

## Memory

| Form | Meaning |
|---|---|
| `size_of::<T>()`, `align_of::<T>()` | Size, alignment |
| `Layout::new::<T>()`, `Layout::array::<T>(n)` | An allocation layout |
| `alloc`, `realloc`, `dealloc` | Memory by hand |
| `MaybeUninit::uninit()`, `assume_init` | Unbuilt memory |
| `ManuallyDrop` | Stopping a drop |
| `ptr::drop_in_place` | Dropping in place |
| `repr(C)`, `repr(transparent)` | A layout promise |
| `PhantomData<T>` | Ownership information |

## Branches

| Form | Meaning |
|---|---|
| `T: Send` | Ownership moves to a branch |
| `T: Sync` | `&T` moves to a branch |
| `unsafe impl Send for T {}` | The promise is yours |
| `AtomicU32::fetch_add` | An atomic increase |
| `compare_exchange(_weak)` | Replace the expected |
| `Relaxed` | Atomicity only |
| `Acquire`, `Release` | Show what was written |
| `UnsafeCell<T>` | The basis of interior mutability |

## Async

| Form | Meaning |
|---|---|
| `impl Future`, `poll` | A future by hand |
| `Poll::Ready(v)`, `Poll::Pending` | A result, not yet |
| `cx.waker().clone()` | A waker to store |
| `wake()`, `wake_by_ref()` | Poll again |
| `impl Wake for T` | A waker from `Arc<T>` |
| `async fn`, `.await` | A state machine |
| `pin!`, `Box::pin` | Pinning |
| `get_unchecked_mut`, `Pin::new_unchecked` | Pin projection |

## Macros

| Form | Meaning |
|---|---|
| `macro_rules! name { (pattern) => { template }; }` | Declarative |
| `$x:expr`, `$t:ty`, `$n:ident`, `$a:tt` | Fragments |
| `$( ... ),* $(,)?` | Repetition, a trailing comma |
| `#[proc_macro]`, `#[proc_macro_derive(N)]` | Procedural |
| `#[proc_macro_attribute]` | One that changes the item |

## FFI

| Form | Meaning |
|---|---|
| `unsafe extern "C" { fn f(); }` | A function from C |
| `safe fn f();` | A safe declaration |
| `#[unsafe(no_mangle)] pub extern "C" fn` | Open to C |
| `CString`, `CStr`, `c"text"` | C strings |
| `Box::into_raw`, `Box::from_raw` | An opaque handle |

## Layers

| Form | Meaning |
|---|---|
| `#![no_std]` | Link to `core` |
| `extern crate alloc;` | `Vec`, `String`, `Box` |
| `#[panic_handler]` | What happens on a panic |
| `#[global_allocator]` | Choose the allocator |
