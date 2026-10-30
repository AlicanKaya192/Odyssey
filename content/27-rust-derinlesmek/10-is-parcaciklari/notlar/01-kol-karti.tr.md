## Yazımlar

| İş | Yazım |
|---|---|
| Kol aç | <code>thread::spawn(move &#124;&#124; ...)</code> |
| Bekle | `handle.join().unwrap()` |
| Kapsamlı | <code>thread::scope(&#124;s&#124; { s.spawn(&#124;&#124; ...); })</code> |
| Uyu | `thread::sleep(Duration::from_millis(10))` |
| Kanal | `let (tx, rx) = mpsc::channel();` |
| Gönder | `tx.send(v).unwrap()` |
| Al, bekleyerek | `rx.recv()` |
| Al, beklemeden | `rx.try_recv()` |
| Süreli | `rx.recv_timeout(d)` |
| Çok gönderen | `tx.clone()` |
| Sınırlı kanal | `mpsc::sync_channel(n)` |

## Hangisi?

| İş | Seçim |
|---|---|
| Listeyi paralel işle | `thread::scope` |
| Uzun yaşayan arka plan işi | `spawn` |
| Birden çok üreticiden sonuç topla | Kanal |
| Ortak durum güncelle | `Arc<Mutex<T>>` (bölüm 11) |
| Çok sayıda ağ bağlantısı | async (İleri modül) |

## Hatalar

| Kod | Anlamı | Çözüm |
|---|---|---|
| `E0373` | Closure ödünç alıyor | `move` ya da `scope` |
| `E0382` | Kola verilen ya da gönderilen değer kullanıldı | `clone` ya da sırayı değiştir |
| `E0277` | Tür `Send` değil | `Rc` yerine `Arc` |

## Çekirdek sayısı

`thread::available_parallelism()` kaç kol mantıklı olduğunu söyler. Çekirdekten çok kol açmak işlemci işinde hız kazandırmaz.
