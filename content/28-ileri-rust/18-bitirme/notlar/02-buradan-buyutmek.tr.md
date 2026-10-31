## Eklenebilecekler

| Özellik | Fikir |
|---|---|
| `block_on` | `main`'de tek future için, sonucu döndüren |
| Sınırlı kanal | Dolunca `send` de future olur, gönderen bekler |
| `select` | 10. bölümdeki `Select`, kanalla ve `Sleep`'le |
| Zaman aşımı | `select(future, timers.sleep(ms))` |
| Görev iptali | `JoinHandle` düşünce görevi kuyruğa almama |
| İki işçi kol | `Receiver`'ı `Arc<Mutex<...>>` içinde paylaşmak |

Kolaydan zora sıralı. Her biri küçük, ama testini yazmadan güvenme: Eşzamanlı kodda bir kez geçmek kanıt değildir.

## Gerçek çalışma ortamı nerede ayrılır?

| Konu | Bizimki | Gerçeği |
|---|---|---|
| Ağ | Yok | İşletim sistemi olay mekanizması |
| Kuyruk | `mpsc` kanalı | İşçi başına kilitsiz kuyruk |
| İşçi | Tek kol | Çekirdek sayısı kadar, iş çalma |
| Görev | `Arc<Task>` + `Mutex` | Tek ayırmalı görev, durum makinesi |
| Zamanlayıcı | `BinaryHeap` | Zaman çarkı (timer wheel) |
| Adalet | Kuyruk sırası | Görev başına bütçe |

## Hataları bulmak

| Araç | Ne bulur |
|---|---|
| `cargo test` | Mantık hataları |
| `miri` | `unsafe`'teki tanımsız davranış |
| `loom` | Bütün sıralamaları dener |
| `ThreadSanitizer` | Veri yarışları |

Bu patikada kurulu değiller, adlarını bilmen yeter. `Ring` gibi bir yapıyı gerçekten yayınlayacaksan `miri` ve `loom` zorunlu sayılır.

## Bu kodu üretimde kullanmalı mı?

Hayır. Amacı öğretmektir. Üretimde `tokio`, `crossbeam` gibi yıllardır çalışan kütüphaneler kullanılır. Ama artık onların belgelerini okuduğunda `Waker`, `Pin`, `Send` ya da `Acquire` yabancı gelmeyecek, hata ayıklarken de nereye bakacağını bileceksin. Kazancın kod değil, bu.
