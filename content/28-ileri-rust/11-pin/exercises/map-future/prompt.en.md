Write `Future` for `Map<F, C>`. `inner` is pinned; `func` is not, and comes out with `Option::take`. When `inner` finishes, give the result to `func`, and return its value with `Ready`.
