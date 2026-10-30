`main.rs` ve `stats.rs` senin. `stats.rs`'te `pub fn mean(values: &[f64]) -> Option<f64>` yaz (boşsa `None`). `main.rs`'te modülü bağla ve `mean(&[1.0, 2.0, 6.0])` sonucunu `{:?}` ile yazdır.
