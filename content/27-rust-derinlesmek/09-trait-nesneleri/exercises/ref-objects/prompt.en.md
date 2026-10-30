Write `trait Item { fn price(&self) -> u32; }`, `Book { pages: u32 }` (price `pages / 10`), `Pen` (price 2). `fn total(items: &[&dyn Item]) -> u32` adds up. No boxes.
