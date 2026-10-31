Write `Future` for `Limit<F>`, without requiring `Unpin`. The result is `Option<F::Output>`: `None` if no `left` remains. Otherwise decrease `left` and poll `inner`; if it finishes, `Some(value)`.
