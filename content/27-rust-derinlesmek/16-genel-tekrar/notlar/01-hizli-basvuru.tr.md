## Generic ve trait

| Yazım | Anlamı |
|---|---|
| `fn f<T: Ord>(x: T)` | Sınırlı generic |
| `fn f(x: impl Ord)` | Kısa yazım |
| `where T: Ord + Clone` | Uzun sınırlar |
| `impl<T: Display> Tr for W<T>` | Genel uygulama |
| `type Item;` | İlişkili tür |
| `Box<dyn Tr>`, `&dyn Tr` | Trait nesnesi |

## Ömür

| Yazım | Anlamı |
|---|---|
| `fn f<'a>(x: &'a str) -> &'a str` | Çıktı girdiden ödünç |
| `struct S<'a> { t: &'a str }` | Yapı ödünç tutuyor |
| `&'static str` | Program boyunca yaşar |

## Kapanış ve iterator

| Yazım | Anlamı |
|---|---|
| `Fn`, `FnMut`, `FnOnce` | Oku, değiştir, tüket |
| <code>move &#124;x&#124; ...</code> | Sahipliği içeri al |
| `impl Iterator<Item = T>` | Iterator döndür |
| `.iter()`, `.iter_mut()`, `.into_iter()` | Ödünç, değişken ödünç, sahiplik |
| `.map().filter().collect()` | Tembel zincir, eylemle biter |
| <code>.fold(0, &#124;a, b&#124; a + b)</code> | Biriktir |

## İşaretçi ve paylaşım

| Tür | İş |
|---|---|
| `Box<T>` | Öbekte tek sahip |
| `Rc<T>`, `Rc::clone` | Çok sahip, tek kol |
| `RefCell<T>` | Çalışma anında ödünç denetimi |
| `Weak<T>` | Sahip olmayan bağ |
| `Arc<T>` | Çok sahip, çok kol |
| `Mutex<T>`, `.lock()` | Tek erişim |
| `RwLock<T>` | Çok okuyucu ya da tek yazıcı |

## Kol

| Yazım | İş |
|---|---|
| <code>thread::spawn(move &#124;&#124; ...)</code> | Yeni kol, `join` bekler |
| <code>thread::scope(&#124;s&#124; s.spawn(...))</code> | Ödünçle çalışan kollar |
| `mpsc::channel()` | Gönderen, alan |

## Test ve araç

| Komut ya da yazım | İş |
|---|---|
| `#[test]`, `assert_eq!` | Test |
| `#[should_panic(expected = "...")]` | Panik bekle |
| `cargo clippy`, `cargo fmt` | Denetle, biçimle |
| `cargo run -p app`, `--features x` | Üye ve feature |

## Hata

| Yazım | İş |
|---|---|
| `impl std::error::Error for E {}` | Hata türü |
| `impl From<A> for E` | `?` çevirsin |
| `fn source(&self)` | Sebep |
| `Box<dyn Error>` | Her hata |
