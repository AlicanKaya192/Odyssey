Write `fn two_sums(left: &[i32], right: &[i32]) -> (i32, i32)`: each slice is added on its own branch. Since the inputs are borrowed, `thread::scope` is needed.
