## Parçalara bölüp topla

Listeyi dilimlere ayır, her dilimi ayrı kolda işle, sonuçları birleştir:

```rust
use std::thread;

fn parallel_sum(list: &[i32], parts: usize) -> i32 {
    let size = list.len().div_ceil(parts).max(1);
    thread::scope(|s| {
        let handles: Vec<_> = list
            .chunks(size)
            .map(|part| s.spawn(move || part.iter().sum::<i32>()))
            .collect();
        handles.into_iter().map(|h| h.join().unwrap()).sum()
    })
}

fn main() {
    let list: Vec<i32> = (1..=100).collect();
    println!("{}", parallel_sum(&list, 4));
}
```

```text
5050
```

`chunks` listeyi kopyalamadan böler. `scope` sayesinde kollar dilimleri ödünç alır.

## Çalışan havuzu (fikir)

Bir kanalda işler, birkaç kolda çalışanlar. Standart kütüphanede hazır havuz yoktur. Alanın tek olması gerektiği için paylaşım `Mutex` ister; bölüm 11'de göreceğiz.

## Sıra güvencesi

| Yöntem | Sıra |
|---|---|
| Tutamakları sırayla `join` | Başlatma sırası |
| Kanaldan almak | Bitiş sırası, belirsiz |
| Kanal + sıra numarası | Sonra sıralarsın |

**Sırası belirsiz çıktıyı testte karşılaştırma:** Önce sırala. Bir kez geçen test tesadüf olabilir.

## Sık hatalar

- **Kolu beklememek:** `main` biter, iş yarıda kalır.
- **`tx`'i kapatmamak:** `for x in rx` asılı kalır.
- **`thread::sleep` ile eşitlemek:** Her makinede farklı. `join` ya da kanal kullan.
- **Küçük iş için kol açmak:** Kol açmanın da bedeli var; yalnızca iş yeterince büyükse kazandırır.
