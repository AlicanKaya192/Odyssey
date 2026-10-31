`Limit<F>` için `Future` yaz, `Unpin` isteme. Sonuç `Option<F::Output>`: `left` kalmadıysa `None`. Değilse `left`'i azalt, `inner`'ı yokla; biterse `Some(değer)`.
