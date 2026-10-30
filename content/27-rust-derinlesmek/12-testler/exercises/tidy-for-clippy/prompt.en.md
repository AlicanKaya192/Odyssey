The code works, but Clippy complains. Fix it: the parameter is `&[i32]`, `total` with an iterator, `is_empty_list` a single expression `list.is_empty()`. No `return` and no `0..` left.
