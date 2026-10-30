`double_in_parts(list)`: split the list in two, and in two `thread::scope` branches multiply each part's items by 2. Use `SendPtr` and `get`. Do not write `split_at_mut` or `chunks_mut`.
