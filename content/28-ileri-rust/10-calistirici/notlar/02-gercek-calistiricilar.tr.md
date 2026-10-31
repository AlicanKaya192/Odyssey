## Bizimkinde eksik olan

Yazdığımız çalıştırıcı fikri doğru gösterir ama gerçek işte yetmez:

| Bizimki | Gerçek çalıştırıcı |
|---|---|
| Her zamanlayıcı için bir kol | Tek zamanlayıcı kolu, sıralı süre listesi |
| Tek kolda yoklama | Çekirdek sayısı kadar işçi kol |
| Ortak tek kuyruk | İşçi başına kuyruk, boş işçi başkasından iş çalar (work stealing) |
| Ağ desteği yok | İşletim sisteminin olay mekanizması |
| Görevin sonucu alınamıyor | `spawn` beklenebilir bir tutamaç döndürür |

## Ağı kim uyandırır?

`Timer` için kol açtık, ama on bin bağlantıya on bin kol açarsak başa döneriz. İşletim sistemleri bunun için tek kolla binlerce kaynağı izleme imkânı verir:

| Sistem | Mekanizma |
|---|---|
| Linux | `epoll` |
| macOS | `kqueue` |
| Windows | IOCP |

Çalıştırıcının bu parçasına **reactor** denir. "Şu bağlantıda veri var" haberi gelince ilgili waker'ı çağırır. Future tarafı değişmez: Waker'ı saklar, `Pending` döner.

## Neden dilde hazır değil?

Küçük bir gömülü cihazla büyük bir sunucunun ihtiyacı farklıdır. Rust yalnızca `Future` ve `Waker` sözleşmesini verir, çalıştırıcıyı sana bırakır. Bu yüzden `async` kod çekirdeksiz yerde bile çalışabilir.

## Bilinen adlar

| Crate | Nerede |
|---|---|
| `tokio` | Ağ ve sunucu; en yaygını |
| `smol` | Küçük, sade |
| `embassy` | Gömülü sistemler |

## Uzun iş ne olacak?

Çalıştırıcının kolunda uzun hesap yapmak öteki görevleri durdurur. Çözüm, işi ayrı bir kola vermek ve bitmesini future olarak beklemektir. Bizim `Timer` tam bu şekli kullanıyor: İş kolda, haber waker'la. `oneshot` alıştırması da aynı köprüdür.
