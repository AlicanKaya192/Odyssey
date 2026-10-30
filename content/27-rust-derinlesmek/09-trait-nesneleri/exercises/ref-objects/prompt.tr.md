`trait Item { fn price(&self) -> u32; }`, `Book { pages: u32 }` (fiyat `pages / 10`), `Pen` (fiyat 2) yaz. `fn total(items: &[&dyn Item]) -> u32` toplasın. Kutu yok.
