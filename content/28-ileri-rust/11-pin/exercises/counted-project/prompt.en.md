Write `Future` for `Counted<F>`. `F: Future` is enough; do not require `Unpin`. Increase `polls`, poll `inner` with pin projection, and return the result as is.
