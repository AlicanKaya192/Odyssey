## Generics and traits

| Written | Meaning |
|---|---|
| `fn f<T: Ord>(x: T)` | A bounded generic |
| `fn f(x: impl Ord)` | The short form |
| `where T: Ord + Clone` | Long bounds |
| `impl<T: Display> Tr for W<T>` | A blanket implementation |
| `type Item;` | An associated type |
| `Box<dyn Tr>`, `&dyn Tr` | A trait object |

## Lifetimes

| Written | Meaning |
|---|---|
| `fn f<'a>(x: &'a str) -> &'a str` | The output borrows from the input |
| `struct S<'a> { t: &'a str }` | The struct holds a borrow |
| `&'static str` | Lives for the whole program |

## Closures and iterators

| Written | Meaning |
|---|---|
| `Fn`, `FnMut`, `FnOnce` | Read, change, consume |
| <code>move &#124;x&#124; ...</code> | Take ownership inside |
| `impl Iterator<Item = T>` | Return an iterator |
| `.iter()`, `.iter_mut()`, `.into_iter()` | Borrow, mutable borrow, ownership |
| `.map().filter().collect()` | A lazy chain, ending with an action |
| <code>.fold(0, &#124;a, b&#124; a + b)</code> | Accumulate |

## Pointers and sharing

| Type | Job |
|---|---|
| `Box<T>` | One owner on the heap |
| `Rc<T>`, `Rc::clone` | Many owners, one branch |
| `RefCell<T>` | Borrow checks at run time |
| `Weak<T>` | A link without ownership |
| `Arc<T>` | Many owners, many branches |
| `Mutex<T>`, `.lock()` | One access |
| `RwLock<T>` | Many readers or one writer |

## Branches

| Written | Job |
|---|---|
| <code>thread::spawn(move &#124;&#124; ...)</code> | A new branch, `join` waits |
| <code>thread::scope(&#124;s&#124; s.spawn(...))</code> | Branches working with borrows |
| `mpsc::channel()` | A sender, a receiver |

## Tests and tools

| Command or form | Job |
|---|---|
| `#[test]`, `assert_eq!` | A test |
| `#[should_panic(expected = "...")]` | Expect a panic |
| `cargo clippy`, `cargo fmt` | Check, format |
| `cargo run -p app`, `--features x` | A member and a feature |

## Errors

| Written | Job |
|---|---|
| `impl std::error::Error for E {}` | An error type |
| `impl From<A> for E` | So `?` converts |
| `fn source(&self)` | The cause |
| `Box<dyn Error>` | Any error |
