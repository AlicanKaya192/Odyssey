## Çalışan havuzu

Bir kanalda işler, sabit sayıda çalışan. `rx` tek olduğu için `Arc<Mutex<...>>` ile paylaşılır:

```rust
use std::sync::{mpsc, Arc, Mutex};
use std::thread;

fn main() {
    let (job_tx, job_rx) = mpsc::channel::<i32>();
    let (out_tx, out_rx) = mpsc::channel();
    let job_rx = Arc::new(Mutex::new(job_rx));
    for _ in 0..3 {
        let job_rx = Arc::clone(&job_rx);
        let out_tx = out_tx.clone();
        thread::spawn(move || loop {
            let job = job_rx.lock().unwrap().recv();
            match job {
                Ok(n) => out_tx.send(n * n).unwrap(),
                Err(_) => break,
            }
        });
    }
    drop(out_tx);
    for n in 1..=5 {
        job_tx.send(n).unwrap();
    }
    drop(job_tx);
    let mut got: Vec<i32> = out_rx.iter().collect();
    got.sort();
    println!("{:?}", got);
}
```

```text
[1, 4, 9, 16, 25]
```

Akış:

<figure class="fig"><div class="flow"><span class="node">main: send</span><span class="arrow">→</span><span class="node">Arc&lt;Mutex&lt;rx&gt;&gt;</span><span class="arrow">→</span><span class="node ok">çalışan</span><span class="arrow">→</span><span class="node">sonuç kanalı</span></div><figcaption>Çalışanlar sırayla iş alır, sonuçları ayrı kanala yazar.</figcaption></figure>

**Dikkat:** `let job = rx.lock().unwrap().recv();` satırı koruyucuyu o satır bitince bırakır. `while let Ok(job) = rx.lock().unwrap().recv()` yazılsaydı kilit döngü gövdesi boyunca tutulur ve işler aynı anda yapılmazdı. Bu, gerçek programlarda sık görülen bir hatadır.

## Küçük kurallar

- Kilit tutarken `println!` da yavaştır, dosya ya da ağ daha da yavaş.
- Kilit tutarken closure çağırma: İçinde ne olduğunu bilmiyorsun.
- `.lock().unwrap()` tek satırda kalabilir: Koruyucu satır sonunda düşer.
- Bir `Vec<Mutex<T>>` tek büyük kilitten daha iyi ölçeklenebilir.
