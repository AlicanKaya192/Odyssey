Write `Iterator` for `struct Windows2<'a, T> { items: &'a [T], index: usize }`: it gives slices of two neighbors. `[1, 2, 3]` gives `[1, 2]`, `[2, 3]`. Do not use `windows`.
